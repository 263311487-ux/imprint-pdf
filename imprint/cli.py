"""Imprint command-line interface."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .converter import build_document, md_to_html
from .fonts import missing_font_slots
from .recommend import recommend_theme
from .render import compress_pdf, render_pdf
from .theme import theme_css
from .themes import list_themes
from .validator import validate_pdf


def _enable_utf8_io() -> None:
    """Windows consoles default to a legacy codepage; force UTF-8 output so
    Chinese report text never crashes print()."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="imprint",
        description="AI 原生 · 印刷级中文 PDF 生成器：Markdown 进，出版社级 PDF 出，自带 0-100 印刷级质检报告。",
    )
    p.add_argument("input", nargs="?", default=None, help="输入 Markdown 文件（支持 frontmatter: title/author/date/subtitle/keywords/theme）")
    p.add_argument("-o", "--output", default=None, help="输出 PDF 路径（默认 input.pdf）")
    p.add_argument("--theme", default=None, help="主题名（默认读 frontmatter 或 modern）")
    p.add_argument("--themes-dir", default=None, help="额外主题目录（*.json）")
    p.add_argument("--no-validate", action="store_true", help="跳过印刷级质检")
    p.add_argument("--report", default=None, help="把质检报告另存为 JSON")
    p.add_argument("--compress", action="store_true", help="生成后激进压缩（清除冗余对象）")
    p.add_argument("--no-pdf-ua", action="store_true", help="不输出 PDF/UA 标签版")
    p.add_argument("--new", metavar="TEMPLATE", default=None, help="从模板生成新文档: report/book/resume/techdoc/letter")
    p.add_argument("--list-templates", action="store_true", help="列出可用模板")
    p.add_argument("--list-themes", action="store_true", help="列出可用主题")
    p.add_argument("--version", action="version", version=f"imprint {__version__}")
    return p


def _new_document(template: str, out: Path | None) -> int:
    from importlib.resources import files

    tpl = template.removesuffix(".md")
    path = Path(str(files("imprint.templates").joinpath(f"{tpl}.md")))
    if not path.exists():
        print(f"错误: 模板 {template} 不存在（可用: {list_templates()}）", file=sys.stderr)
        return 1
    target = out or Path(f"{tpl}.md")
    target.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"已生成 {target}，渲染: imprint {target}")
    return 0


def list_templates() -> str:
    from importlib.resources import files

    tpl_dir = files("imprint.templates")
    names = sorted(
        p.name.removesuffix(".md")
        for p in tpl_dir.iterdir()
        if p.name.endswith(".md")
    )
    return " / ".join(names)


def main(argv: list[str] | None = None) -> int:
    _enable_utf8_io()
    args = build_parser().parse_args(argv)
    if args.list_templates:
        print(list_templates())
        return 0
    if args.new:
        return _new_document(args.new, Path(args.output) if args.output else None)
    if args.list_themes:
        for name in list_themes(args.themes_dir):
            print(name)
        return 0

    if not args.input:
        build_parser().print_help()
        return 1
    src = Path(args.input)
    if not src.exists():
        print(f"错误: 找不到输入文件 {src}", file=sys.stderr)
        return 1

    conv = md_to_html(src.read_text(encoding="utf-8"))
    meta = conv.meta
    theme_name = args.theme or (meta.get("theme") or "").strip().lower()
    theme_note = None
    if not theme_name:
        theme_name, theme_note = recommend_theme(meta, conv.text)
    css, theme = theme_css(theme_name, args.themes_dir)
    if theme_note:
        print(f"主题：{theme_name}（{theme_note}）")
    html = build_document(conv)

    for slot in missing_font_slots(theme):
        print(f"警告: 主题 {theme_name} 的{slot}字体在本机不可用，已回退系统字体", file=sys.stderr)

    out = Path(args.output) if args.output else src.with_suffix(".pdf")
    out.parent.mkdir(parents=True, exist_ok=True)
    pages = render_pdf(html, css, out, pdf_ua=not args.no_pdf_ua, base_url=src.parent)
    if args.compress:
        saved = compress_pdf(out)
        print(f"已压缩，节省 {saved/1024:.0f} KB" if saved else "无图片可压缩，文件保持原样")

    if args.no_validate:
        print(f"已生成 {out}（{pages} 页，主题 {theme_name}）")
        return 0

    report = validate_pdf(
        out,
        toc_entries=[] if str(meta.get("layout") or "").strip().lower() == "gongwen" else [(i.text, i.href) for i in conv.toc],
        serif_hint=meta.get("theme-font-hint") or "Songti",
        theme_colors=theme["tokens"].get("color"),
    )
    print(report.print_table())
    if args.report:
        Path(args.report).write_text(
            json.dumps(report.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    return 0 if report.score >= 80 else 1


if __name__ == "__main__":
    raise SystemExit(main())
