"""Markdown -> semantic HTML, ready for print-grade rendering."""

from __future__ import annotations

import html
import re
from dataclasses import dataclass, field
from typing import Any

import yaml
from markdown_it import MarkdownIt
from markdown_it.token import Token
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.tasklists import tasklists_plugin
from mdit_py_plugins.texmath import texmath_plugin
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.util import ClassNotFound


@dataclass
class TocItem:
    level: int
    text: str
    href: str


@dataclass
class Conversion:
    html: str
    meta: dict[str, Any] = field(default_factory=dict)
    toc: list[TocItem] = field(default_factory=list)
    text: str = ""


def _mermaid_aware_fence(orig_fence):
    """Render ```mermaid fences to SVG figures, keep everything else as-is."""

    def fence(tokens, idx, options, env):
        info = (tokens[idx].info or "").strip()
        lang = info.split(maxsplit=1)[0].lower() if info else ""
        if lang == "mermaid":
            return _render_mermaid(tokens[idx].content)
        return orig_fence(tokens, idx, options, env)

    return fence


def _render_mermaid(code: str) -> str:
    """Render a ```mermaid block to an embedded SVG figure (charts extra)."""
    try:
        import base64

        import mermaidx
    except Exception:
        return f'<pre><code class="language-mermaid">{html.escape(code)}</code></pre>'
    try:
        svg = _svg_fix_size(mermaidx.render(code).svg())
        b64 = base64.b64encode(svg.encode("utf-8")).decode()
        return (
            '<figure class="mermaid-figure">'
            f'<img src="data:image/svg+xml;base64,{b64}" alt="mermaid 图"/>'
            "</figure>"
        )
    except Exception:
        return f'<pre><code class="language-mermaid">{html.escape(code)}</code></pre>'


def _svg_fix_size(svg: str) -> str:
    """Give the SVG an explicit pixel size from its viewBox (print-stable)."""
    m = re.search(r'viewBox="([-\d.]+) ([-\d.]+) ([\d.]+) ([\d.]+)"', svg)
    if not m:
        return svg
    _, _, w, h = (float(x) for x in m.groups())
    return re.sub(
        r'width="100%"',
        f'width="{w:.0f}px" height="{h:.0f}px"',
        svg,
        count=1,
    )


def _highlight(code: str, lang: str, attrs: str) -> str:
    lang = (lang or "").strip().lower()
    try:
        if lang:
            lexer = get_lexer_by_name(lang)
        else:
            lexer = guess_lexer(code)
    except ClassNotFound:
        lexer = None
    if lexer is None:
        return f'<pre><code>{html.escape(code)}</code></pre>'
    formatter = HtmlFormatter(nowrap=False)
    return highlight(code, lexer, formatter)


_CJK_HEADING = re.compile(r"[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]")
_LATIN_RATIO = re.compile(r"[A-Za-z]")


def _is_latin_block(text: str) -> bool:
    latin = len(_LATIN_RATIO.findall(text))
    if not latin:
        return False
    cjk = len(_CJK_HEADING.findall(text))
    return latin > cjk * 2 and latin >= 12


def _slugify(text: str, used: set[str]) -> str:
    base = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff\u00c0-\u024f-]+", "-", text).strip("-").lower()
    if not base:
        base = "sec"
    slug, i = base, 2
    while slug in used:
        slug = f"{base}-{i}"
        i += 1
    used.add(slug)
    return slug



ALERT_TYPES = {
    "NOTE": ("note", "提示"),
    "TIP": ("tip", "建议"),
    "IMPORTANT": ("important", "重要"),
    "WARNING": ("warning", "警告"),
    "CAUTION": ("caution", "小心"),
}


def _alerts_plugin(md: MarkdownIt) -> None:
    """GitHub-style blockquote alerts: `> [!NOTE]`, `> [!WARNING]`, ..."""

    def _scan(state) -> None:
        tokens = state.tokens
        for i, tok in enumerate(tokens):
            if tok.type != "blockquote_open":
                continue
            j = i + 1
            if j >= len(tokens) or tokens[j].type != "paragraph_open":
                continue
            inline = tokens[j + 1] if j + 1 < len(tokens) and tokens[j + 1].type == "inline" else None
            if inline is None or not inline.children:
                continue
            first = next((ch for ch in inline.children if ch.type == "text"), None)
            if first is None:
                continue
            m = re.match(r"^\s*\[!([A-Z]+)\](?:\s+|$)", first.content)
            if not m:
                continue
            key = m.group(1).upper()
            if key not in ALERT_TYPES:
                continue
            css_class, label = ALERT_TYPES[key]
            tok.attrSet("class", f"alert alert-{css_class}")
            tok.attrSet("data-label", label)
            first.content = first.content[m.end():].lstrip()
            inline.content = "".join(ch.content for ch in inline.children)

    md.core.ruler.after("inline", "imprint_alerts", _scan)



def _render_math(latex: str, display: bool) -> str:
    """Render a LaTeX math expression to an embedded SVG (font-independent)."""
    latex = latex.strip()
    try:
        import base64
        import io

        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig = plt.figure(figsize=(0.01, 0.01))
        fig.text(0.5, 0.5, f"${latex}$", fontsize=20 if display else 16)
        buf = io.BytesIO()
        fig.savefig(
            buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.02
        )
        plt.close(fig)
        svg = buf.getvalue().decode("utf-8")
        # matplotlib embeds the raw LaTeX as XML comments; drop them or
        # WeasyPrint renders them as visible text.
        svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
        b64 = base64.b64encode(svg.encode("utf-8")).decode()
        img = f'<img class="math-{"display" if display else "inline"}" src="data:image/svg+xml;base64,{b64}" alt=""/>'
        if display:
            return f'<div class="math-display">{img}</div>'
        return img
    except Exception:
        return f"<code>${latex}$</code>"


def _install_math_renderer(md: MarkdownIt) -> None:
    md.renderer.rules["math_inline"] = lambda tokens, idx, options, env: _render_math(
        tokens[idx].content, False
    )
    md.renderer.rules["math_block"] = lambda tokens, idx, options, env: _render_math(
        tokens[idx].content, True
    )


def _install_footnote_renderer(md: MarkdownIt) -> None:
    """Footnote backrefs default to U+21A9+FE0E (↩︎), which most CJK fonts
    lack (Pango falls back to LastResort = tofu). Use U+2191 (↑), covered by
    every font in the theme stacks, and drop the variation selector."""

    def _backref(tokens, idx, options, env):
        ident = md.renderer.rules["footnote_anchor_name"](tokens, idx, options, env)
        if tokens[idx].meta["subId"] > 0:
            ident += ":" + str(tokens[idx].meta["subId"])
        return ' <a href="#fnref' + ident + '" class="footnote-backref">\u2191</a>'

    md.renderer.rules["footnote_anchor"] = _backref


def md_to_html(md_text: str) -> Conversion:
    md = (
        MarkdownIt("commonmark", {"highlight": _highlight})
        .enable("table")
        .use(front_matter_plugin)
        .use(footnote_plugin)
        .use(tasklists_plugin)
        .use(texmath_plugin, delimiters="dollars")
        .use(_alerts_plugin)
    )
    md.renderer.rules["fence"] = _mermaid_aware_fence(md.renderer.rules["fence"])
    _install_math_renderer(md)
    _install_footnote_renderer(md)
    tokens = md.parse(md_text)
    meta: dict[str, Any] = {}
    body_tokens: list[Token] = []
    for tok in tokens:
        if tok.type == "front_matter":
            try:
                parsed = yaml.safe_load(tok.content)
                if isinstance(parsed, dict):
                    meta = parsed
            except yaml.YAMLError:
                pass
        else:
            body_tokens.append(tok)

    # mutate tokens: heading ids + TOC collection + latin block lang
    used_ids: set[str] = set()
    toc: list[TocItem] = []
    for i, tok in enumerate(body_tokens):
        if tok.type == "heading_open":
            level = int(tok.tag[1])
            inline = body_tokens[i + 1] if i + 1 < len(body_tokens) else None
            text = (
                "".join(t.content for t in inline.children if t.type == "text")
                if inline and inline.children
                else ""
            )
            slug = _slugify(text, used_ids)
            tok.attrSet("id", slug)
            if level <= 3:
                toc.append(TocItem(level=level, text=text or slug, href=f"#{slug}"))
        elif tok.type == "paragraph_open":
            inline = body_tokens[i + 1] if i + 1 < len(body_tokens) else None
            raw = (
                "".join(t.content for t in inline.children if t.type in ("text", "code_inline"))
                if inline and inline.children
                else ""
            )
            if _is_latin_block(raw):
                tok.attrSet("lang", "en")

    body = md.renderer.render(body_tokens, md.options, {})
    body = _polish_html(body)
    plain = "\n".join(
        tok.content for tok in body_tokens if tok.type in ("inline", "text")
    )
    return Conversion(html=body, meta=meta, toc=toc, text=plain)


def _polish_html(body: str) -> str:
    """Print-oriented post-processing of the rendered HTML body."""
    # chapter-leading paragraphs: first paragraph after an h1 is not indented (Chinese convention)
    out: list[str] = []
    for part in re.split(r"(<h1[^>]*>.*?</h1>)", body, flags=re.S):
        if not part:
            continue
        if part.startswith("<h1"):
            out.append(part)
            continue
        part = re.sub(r"<p>", '<p class="first">', part, count=1)
        out.append(part)
    body = "".join(out)
    # code blocks: expose language for a print label
    body = re.sub(
        r'<pre><code class="language-([\w+-]+)">',
        lambda m: f'<pre class="code-block" data-lang="{html.escape(m.group(1).upper())}"><code class="language-{m.group(1)}">',
        body,
    )
    # bare images in paragraphs: keep the paragraph centered
    body = re.sub(r"<p><img ([^>]*)></p>", r'<p class="figure"><img \1></p>', body)
    return body


def _cover_html(meta: dict) -> str:
    if not meta.get("title"):
        return ""
    title = html.escape(str(meta["title"]))
    subtitle = html.escape(str(meta["subtitle"])) if meta.get("subtitle") else ""
    author = html.escape(str(meta["author"])) if meta.get("author") else ""
    date = html.escape(str(meta["date"])) if meta.get("date") else ""
    parts = ['<section class="cover">', '<p class="brand">IMPRINT · 印 记</p>', f'<h1 class="title">{title}</h1>']
    if subtitle:
        parts.append(f'<p class="subtitle">{subtitle}</p>')
    parts.append('<div class="rule"></div>')
    if author or date:
        parts.append('<p class="meta">')
        if author:
            parts.append(f'<span class="author">{author}</span><br/>')
        if date:
            parts.append(date)
        parts.append("</p>")
    parts.append("</section>")
    return "".join(parts)


def _toc_html(toc: list[TocItem]) -> str:
    if not toc:
        return ""
    lis = []
    for item in toc:
        level = min(item.level, 3)
        label = html.escape(item.text)
        lis.append(f'<li class="l{level}"><a href="{item.href}">{label}</a></li>')
    return f'<section class="toc-page"><h2>目 录</h2><ul class="toc-list">{"".join(lis)}</ul></section>'


def build_document(conv: Conversion) -> str:
    meta = conv.meta
    title = html.escape(str(meta.get("title") or "Untitled"))
    author = html.escape(str(meta.get("author") or ""))
    keywords = html.escape(str(meta.get("keywords") or ""))
    description = html.escape(str(meta.get("description") or meta.get("subtitle") or ""))
    meta_tags = (
        f'<meta name="author" content="{author}"/>'
        f'<meta name="keywords" content="{keywords}"/>'
        f'<meta name="description" content="{description}"/>'
    )
    booktitle_css = f'main.content {{ string-set: booktitle "{title}"; }}'
    cover = _cover_html(meta)
    toc = _toc_html(conv.toc)
    body = conv.html
    # mark first h1 as .first so it doesn't force a blank page after the TOC
    body = re.sub(r'<h1', '<h1 class="first"', body, count=1)
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<title>{title}</title>
{meta_tags}
<style>{booktitle_css}</style>
</head>
<body>
{cover}
{toc}
<main class="content">
{body}
</main>
</body>
</html>"""
