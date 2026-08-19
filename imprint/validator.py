"""Print-grade quality scorer: 0-100 with machine-checkable evidence."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import pymupdf as fitz  # PyMuPDF
import pdfplumber


@dataclass
class CheckResult:
    key: str
    label: str
    max_score: float
    score: float = 0.0
    passed: bool = False
    evidence: str = ""

    def to_dict(self) -> dict:
        return {
            "key": self.key,
            "label": self.label,
            "max": self.max_score,
            "score": round(self.score, 1),
            "passed": self.passed,
            "evidence": self.evidence,
        }


@dataclass
class ValidationReport:
    score: float = 0.0
    grade: str = "D"
    pages: int = 0
    size_bytes: int = 0
    checks: list[CheckResult] = field(default_factory=list)
    violations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "score": round(self.score, 1),
            "grade": self.grade,
            "pages": self.pages,
            "size_bytes": self.size_bytes,
            "checks": [c.to_dict() for c in self.checks],
            "violations": self.violations,
        }

    def print_table(self) -> str:
        lines = []
        lines.append("印刷级质检报告")
        lines.append("=" * 46)
        for c in self.checks:
            mark = "✓" if c.passed else "✗"
            lines.append(f" {mark} {c.label:<16} {c.score:>5.1f}/{c.max_score:<5.1f}  {c.evidence}")
        lines.append("-" * 46)
        lines.append(f" 总分 {self.score:.1f}/100 · 等级 {self.grade} · {self.pages} 页 · {self.size_bytes/1024:.0f} KB")
        if self.violations:
            lines.append(" 违规清单:")
            for v in self.violations[:10]:
                lines.append(f"   · {v}")
        return "\n".join(lines)


HEAD_BAD = "，。、；：？！）】》」』”’％‰°℃"
END_BAD = "（【《〈「『“‘"

def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        raise ValueError(f"unsupported color: {hex_color}")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def _relative_luminance(hex_color: str) -> float:
    r, g, b = (v / 255 for v in _hex_to_rgb(hex_color))

    def _lin(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def _wcag_ratio(fg: str, bg: str) -> float:
    l1, l2 = _relative_luminance(fg), _relative_luminance(bg)
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)




def _check_glyphs(doc: fitz.Document) -> CheckResult:
    """Detect missing-glyph fallback fonts (LastResort/notdef = tofu boxes)."""
    r = CheckResult("glyph_coverage", "缺字检测", 5)
    bad = set()
    for page in doc:
        for f in page.get_fonts(full=True):
            name = str(f[3]).lower()
            if "lastresort" in name or "notdef" in name or ".notdef" in name:
                bad.add(str(f[3]))
    r.score = 5 if not bad else max(0.0, 5 - 2.5 * len(bad))
    r.passed = not bad
    r.evidence = "无缺字回退" if not bad else "检测到回退字体: " + ", ".join(sorted(bad))
    r.violations = list(bad)
    return r


def _check_overflow(pdf_path: Path) -> CheckResult:
    """Detect content spilling past the page edges (clipped by the trim box)."""
    r = CheckResult("overflow", "内容溢出", 5)
    violations: list[str] = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            if i == 1:
                continue  # cover is full-bleed by design
            if page.width < 100 or page.height < 100:
                continue
            for ch in page.chars:
                if ch["x1"] > page.width + 3 or ch["x0"] < -3 or ch["bottom"] > page.height + 3 or ch["top"] < -3:
                    violations.append(f"第{i}页字符越界: 「{ch['text']}」 x={ch['x1']:.0f}/{page.width:.0f}")
                    break
    r.score = max(0.0, 5 - 2.5 * len(violations))
    r.passed = not violations
    r.evidence = "无内容越界" if not violations else f"{len(violations)} 处越界"
    r.violations = violations
    return r


def _check_image_dpi(doc: fitz.Document) -> CheckResult:
    """Warn when embedded raster images print below 150 DPI."""
    r = CheckResult("image_dpi", "图片清晰度", 5)
    low: list[str] = []
    for pno in range(doc.page_count):
        seen: set[int] = set()
        for img in doc.get_page_images(pno, full=True):
            xref = img[0]
            if xref in seen:
                continue
            seen.add(xref)
            try:
                info = doc.extract_image(xref)
                rects = doc.get_image_rects(xref)
            except Exception:
                continue
            for rect in rects:
                w_in = rect.width / 72.0
                if w_in <= 0:
                    continue
                dpi = info["width"] / w_in
                if dpi < 150:
                    low.append(f"第{pno+1}页图片约 {dpi:.0f} DPI")
                    break
    r.score = max(0.0, 5 - 2.5 * len(low))
    r.passed = not low
    r.evidence = "全部达标" if not low else "; ".join(low[:3])
    r.violations = low
    return r



def _check_contrast(colors: dict) -> CheckResult:
    r = CheckResult("contrast", "主题对比度", 5)
    try:
        ink = colors.get("ink", "#1c1c1e")
        paper = colors.get("paper", "#ffffff")
        accent = colors.get("accent", ink)
        muted = colors.get("muted", ink)
        soft = colors.get("accent-soft", paper)
    except Exception:
        r.evidence = "缺少色板"
        return r
    pairs = [
        ("正文 ink/paper", ink, paper, 7.0),
        ("小字 muted/paper", muted, paper, 4.5),
        ("背景文字 ink/soft", ink, soft, 4.5),
        ("装饰 accent/paper", accent, paper, 3.0),
    ]
    failed = []
    notes = []
    for label, fg, bg, need in pairs:
        try:
            ratio = _wcag_ratio(fg, bg)
        except Exception:
            failed.append(f"{label} 颜色无法解析")
            continue
        notes.append(f"{label} {ratio:.1f}:1")
        if ratio < need:
            failed.append(f"{label} {ratio:.1f}:1 < {need}:1")
    r.score = max(0.0, 5 - 1.25 * len(failed))
    r.passed = not failed
    r.evidence = " · ".join(notes)
    r.violations = failed
    return r




def grade_of(score: float) -> str:
    if score >= 95:
        return "A+"
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    return "D"


def _check_text_selectable(doc: fitz.Document, pages: int) -> CheckResult:
    r = CheckResult("text_selectable", "文本可选", 15)
    if pages == 0:
        r.evidence = "无页面"
        return r
    total = sum(len(p.get_text().strip()) for p in doc)
    avg = total / pages
    r.score = 15 if avg >= 30 else (10 if avg >= 10 else 0)
    r.passed = r.score == 15
    r.evidence = f"平均每页 {avg:.0f} 字符"
    return r


def _check_fonts(doc: fitz.Document) -> CheckResult:
    r = CheckResult("fonts_embedded", "字体子集嵌入", 15)
    seen: dict[str, bool] = {}
    for page in doc:
        try:
            for f in page.get_fonts(full=True):
                if len(f) >= 8:
                    name, embedded = f[3], bool(f[7])
                else:
                    name, embedded = f[3], True
                seen[name] = seen.get(name, True) and embedded
        except Exception:
            continue
    if not seen:
        r.evidence = "未检测到字体"
        return r
    ok = sum(1 for v in seen.values() if v)
    r.score = 15 * ok / len(seen)
    r.passed = r.score >= 14.9
    bad = [n for n, v in seen.items() if not v]
    r.evidence = f"{ok}/{len(seen)} 字体已嵌入" + (f"，未嵌入: {', '.join(bad)}" if bad else "")
    return r


def _check_metadata(meta_title: str | None) -> CheckResult:
    r = CheckResult("metadata", "元数据完整", 3)
    score = 3.0
    notes = []
    if not meta_title or meta_title == "Untitled":
        score -= 1.5
        notes.append("缺标题")
    r.score = max(score, 0)
    r.passed = r.score == 3
    r.evidence = notes[0] if notes else f"标题「{meta_title}」"
    return r


def _check_punctuation(pdf_path: Path) -> CheckResult:
    r = CheckResult("punctuation", "标点避头尾", 15)
    violations: list[str] = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            lines: dict[float, list] = {}
            for ch in page.chars:
                key = round(ch["top"], 1)
                lines.setdefault(key, []).append(ch)
            for top, chars in lines.items():
                chars.sort(key=lambda c: c["x0"])
                text = "".join(c["text"] for c in chars).strip()
                if not text:
                    continue
                if len(text) == 1:
                    # 单字符装饰（引号/项目符号）不参与禁则判定
                    continue
                # 行首禁则字若左侧同一行有内联图形（行内公式等矢量图），
                # 视觉上并非行首，pdfplumber 提取不到图形文字导致误报。
                if text[0] in HEAD_BAD and not _has_art_left(page, top, chars[0]["x0"]):
                    violations.append(f"第{i}页行首「{text[0]}」: {text[:18]}…")
                if text[-1] in END_BAD:
                    violations.append(f"第{i}页行尾「{text[-1]}」: …{text[-18:]}")
    r.score = max(0.0, 15 - 2.5 * len(violations))
    r.passed = not violations
    r.evidence = "0 违规" if not violations else f"{len(violations)} 处违规"
    r.violations = violations
    return r


def _has_art_left(page, line_top: float, first_x0: float) -> bool:
    """True when an inline graphic (e.g. an SVG formula) sits directly left of
    the first text char on this line, so the char is not truly a line start."""
    for kind in ("rect", "curve", "line"):
        for o in page.objects.get(kind, []):
            o_top = o.get("top", 0)
            o_bot = o.get("bottom", o_top)
            if (
                o.get("x1", 0) <= first_x0 + 2
                and o.get("x0", 0) < first_x0 - 3
                and abs(o_top - line_top) < 30
                and (o_bot - o_top) < 30
            ):
                return True
    return False


def _check_widows(pdf_path: Path, toc_labels: list[str]) -> CheckResult:
    r = CheckResult("widows_orphans", "孤行寡行", 9)
    violations: list[str] = []
    footer_re = re.compile(r"^[\s—\-–—\d]+$")
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            words = page.extract_words()
            if not words:
                continue
            if len(page.extract_text_lines() or []) < 8:
                # 封面/目录等稀疏页不做孤行判定
                continue
            last_y = max(w["bottom"] for w in words)
            last_words = [w for w in words if w["bottom"] >= last_y - 2]
            last_text = "".join(w["text"] for w in sorted(last_words, key=lambda w: w["x0"])).strip()
            if not last_text or footer_re.match(last_text) or last_text.replace(".", "").strip() == "":
                continue
            if any(label and label in last_text for label in toc_labels):
                violations.append(f"第{i}页底部标题孤悬: 「{last_text[:20]}」")
    r.score = max(0.0, 9 - 3 * len(violations))
    r.passed = not violations
    r.evidence = "0 处" if not violations else f"{len(violations)} 处"
    r.violations = violations
    return r


def _check_toc(pdf_path: Path, toc_entries: list[tuple[str, str]]) -> CheckResult:
    """Verify TOC labels resolve to the pages listed in the TOC."""
    r = CheckResult("toc", "目录页码", 15)
    if not toc_entries:
        r.passed = True
        r.score = 15
        r.evidence = "无目录（N/A）"
        return r
    with pdfplumber.open(pdf_path) as pdf:
        # locate TOC page: the page whose first words contain the first label
        toc_page_idx: int | None = None
        first_label = toc_entries[0][0]
        for i, page in enumerate(pdf.pages):
            if page.search(first_label) and i < 3:
                toc_page_idx = i
                break
        if toc_page_idx is None:
            r.evidence = "未定位到目录页"
            return r
        toc_words = pdf.pages[toc_page_idx].extract_words()
        by_top: dict[float, list] = {}
        for w in toc_words:
            by_top.setdefault(round(w["top"], 0), []).append(w)
        entries: list[tuple[str, int]] = []
        norm_entries = {re.sub(r"[\s.]+", "", label): label for label, _ in toc_entries}
        for top, ws in by_top.items():
            ws = sorted(ws, key=lambda w: w["x0"])
            text = "".join(w["text"] for w in ws)
            nums = [w["text"] for w in ws if w["text"].isdigit()]
            if not nums:
                continue
            label_norm = re.sub(r"[\s.]+", "", re.sub(r"\d+\s*$", "", text))
            for norm, original in norm_entries.items():
                if label_norm == norm:
                    entries.append((original, int(nums[-1])))
                    break
        if not entries:
            r.evidence = "目录页未解析出页码"
            return r
        actual: dict[str, int] = {}
        outline: dict[str, int] = {}
        with fitz.open(pdf_path) as doc:
            for _lvl, title, page in doc.get_toc():
                norm = re.sub(r"\s+", "", title or "")
                outline[norm] = page
        for label, _href in toc_entries:
            norm = re.sub(r"\s+", "", label)
            if norm in outline:
                actual[label] = outline[norm]
            else:
                actual[label] = _find_heading_page(pdf, toc_page_idx, label)
    mismatches = []
    for label, listed in entries:
        if label in actual and actual[label] != listed:
            mismatches.append(f"「{label}」目录写 {listed} 实际 {actual[label]}")
    r.score = max(0.0, 15 - 5 * len(mismatches))
    r.passed = not mismatches
    r.evidence = f"核对 {len(entries)} 条" if not mismatches else "; ".join(mismatches[:3])
    r.violations = mismatches
    return r


def _find_heading_page(pdf, toc_page_idx: int, label: str) -> int | None:
    """Locate a heading by font size (headings are >= 11.5pt, body is 10.5pt).
    Used only when the PDF outline lacks the entry."""
    import pdfplumber

    with pdfplumber.open(pdf) as pdf_obj:
        for i in range(toc_page_idx + 1, len(pdf_obj.pages)):
            page = pdf_obj.pages[i]
            big = [c for c in page.chars if c.get("size", 0) >= 11.5]
            if not big:
                continue
            by_line: dict[float, list] = {}
            for c in big:
                by_line.setdefault(round(c["top"], 0), []).append(c)
            for cs in by_line.values():
                text = "".join(c["text"] for c in sorted(cs, key=lambda c: c["x0"]))
                if label and re.sub(r"\s+", "", label) in re.sub(r"\s+", "", text):
                    return i + 1
    return None


def _check_page_numbers(pdf_path: Path) -> CheckResult:
    r = CheckResult("page_numbers", "页码存在", 2)
    found = 0
    total = 0
    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        for page in pdf.pages:
            text = page.extract_text() or ""
            if re.search(r"[—\-–·]\s*\d+\s*[—\-–·]|\b第\s*\d+\s*页\b", text):
                found += 1
    r.score = 2 if (total >= 2 and found >= total - 2) else (1 if found else 0)
    r.passed = r.score == 2
    r.evidence = f"{found}/{total} 页含页码"
    return r


def _check_tagged(doc: fitz.Document) -> CheckResult:
    r = CheckResult("pdf_ua", "PDF/UA 标签", 3)
    tagged = False
    try:
        catalog = doc.pdf_catalog()
        mark_info = doc.xref_get_key(catalog, "MarkInfo")
        tagged = "/Marked" in mark_info[1] and "true" in mark_info[1].lower()
    except Exception:
        pass
    r.score = 3 if tagged else 0
    r.passed = tagged
    r.evidence = "Tagged PDF" if tagged else "未开启"
    return r


def _check_size(size_bytes: int) -> CheckResult:
    r = CheckResult("size", "文件体积", 0)
    kb = size_bytes / 1024
    r.score = 0.0
    r.passed = True
    r.evidence = f"{kb:.0f} KB" + ("（偏小）" if kb < 20 else "（偏大）" if kb > 5120 else "")
    return r


def _check_theme_fonts(doc: fitz.Document, serif_hint: str) -> CheckResult:
    r = CheckResult("theme_fonts", "主题字体生效", 3)

    def norm(s: str) -> str:
        # PDF font names are subset-prefixed and hyphenated ("ESSOFH+Times-New-Roman,")
        # while hints are human names ("Times New Roman"); compare on letters/digits.
        return re.sub(r"[^a-z0-9]", "", s.lower())

    hints = [norm(h) for h in re.split(r"[,\"']+", serif_hint) if len(h.strip()) > 2]
    names: set[str] = set()
    for page in doc:
        for f in page.get_fonts(full=True):
            names.add(norm(str(f[3])))
    matched = [h for h in hints if any(h in n for n in names)]
    r.passed = bool(matched)
    r.score = 3 if r.passed else 0
    r.evidence = (
        f"命中 {', '.join(matched[:2])}" if matched else f"未命中 {serif_hint}"
    )
    return r


def validate_pdf(
    pdf_path: str | Path,
    *,
    toc_entries: list[tuple[str, str]] | None = None,
    serif_hint: str = "Songti",
    theme_colors: dict | None = None,
) -> ValidationReport:
    path = Path(pdf_path)
    report = ValidationReport(size_bytes=path.stat().st_size)
    doc = fitz.open(path)
    report.pages = doc.page_count
    checks = [
        _check_text_selectable(doc, report.pages),
        _check_fonts(doc),
        _check_metadata(doc.metadata.get("title")),
        _check_punctuation(path),
        _check_widows(path, [label for label, _ in (toc_entries or [])]),
        _check_toc(path, toc_entries or []),
        _check_page_numbers(path),
        _check_tagged(doc),
        _check_size(report.size_bytes),
        _check_theme_fonts(doc, serif_hint),
        _check_contrast(theme_colors or {}),
        _check_glyphs(doc),
        _check_overflow(path),
        _check_image_dpi(doc),
    ]
    doc.close()
    report.checks = checks
    for c in checks:
        report.score += c.score
        if getattr(c, "violations", None):
            report.violations.extend(c.violations)
    report.grade = grade_of(report.score)
    return report
