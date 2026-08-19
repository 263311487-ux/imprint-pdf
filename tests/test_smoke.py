"""Smoke tests: converter -> PDF -> validator, end to end."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from imprint.converter import _render_mermaid, build_document, md_to_html
from imprint.recommend import recommend_theme
from imprint.render import render_pdf
from imprint.theme import theme_css
from imprint.themes import list_themes, load_theme
from imprint.validator import validate_pdf


ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture()
def sample_md() -> str:
    return (ROOT / "examples" / "sample.md").read_text(encoding="utf-8")


def test_builtin_themes():
    names = list_themes()
    assert {"modern", "academic", "nord", "sepia", "newspaper", "catppuccin", "mono", "jade", "coffee", "ocean", "lavender", "rose", "pine", "wine", "graphite", "midnight", "coral", "amber", "mint", "sand"} <= set(names)
    for name in names:
        theme = load_theme(name)
        assert "tokens" in theme
        assert {"color", "typography", "spacing"} <= set(theme["tokens"])


def test_converter_semantics(sample_md):
    conv = md_to_html(sample_md)
    assert conv.meta["title"] == "印记"
    assert len(conv.toc) >= 4
    assert conv.toc[0].level == 1
    assert conv.toc[0].href.startswith("#")
    html = build_document(conv)
    assert "<section class=\"cover\">" in html
    assert "toc-list" in html
    assert "在计算机诞生的头三十年" in html
    assert "lang=\"en\"" in html  # latin block tagged for hyphenation


def test_end_to_end(sample_md, tmp_path):
    conv = md_to_html(sample_md)
    css, _ = theme_css("modern")
    html = build_document(conv)
    out = tmp_path / "out.pdf"
    pages = render_pdf(html, css, out)
    assert pages >= 4
    report = validate_pdf(
        out,
        toc_entries=[(i.text, i.href) for i in conv.toc],
        serif_hint="Songti",
    )
    assert report.score >= 90, report.print_table()


def test_mermaid_fallback_or_figure():
    conv = md_to_html("# 图\n\n```mermaid\ngraph TD\n  A-->B\n```\n")
    assert 'id="流程图"' not in conv.html  # sanity: heading slug
    try:
        import mermaidx  # noqa: F401

        assert '<figure class="mermaid-figure">' in conv.html
        assert "<pre" not in conv.html[conv.html.find("<figure"):conv.html.find("</figure>") + 9]
    except ImportError:
        assert 'class="language-mermaid"' in conv.html  # graceful fallback


@pytest.mark.parametrize(
    "meta,body,expected",
    [
        ({"title": "项目周报"}, "采集链路扩容，质检模型上线。", "graphite"),
        ({"title": "深度学习研究", "keywords": "论文"}, "本研究提出新方法。", "academic"),
        ({"title": "公司新闻快讯"}, "今日要闻。", "newspaper"),
        ({"title": "夏日随笔"}, "散文三则。", "sepia"),
        ({"title": "机器学习入门教程"}, "本教程从零开始。", "mint"),
        ({"title": "历史考据"}, "古典文献制度沿革。", "wine"),
        ({"title": "普通文档"}, "没有信号的普通内容。", "modern"),
        ({"title": "指定主题", "theme": "ocean"}, "正文。", "ocean"),
    ],
)
def test_theme_recommendation(meta, body, expected):
    theme, reason = recommend_theme(meta, body)
    assert theme == expected, (theme, reason)
    assert reason


def test_math_rendering():
    conv = md_to_html("# 公式\n\n$$E = mc^2$$\n\n行内 $a^2+b^2=c^2$ 公式。\n")
    try:
        import matplotlib  # noqa: F401

        assert 'class="math-display"' in conv.html
        assert 'class="math-inline"' in conv.html
        assert "E = mc^2" not in conv.html  # not left as raw text
    except ImportError:
        assert "<code>" in conv.html  # graceful fallback


def test_footnote_glyph_coverage():
    """Footnote backrefs must not use U+21A9/U+FE0E (missing in CJK fonts,
    which makes Pango fall back to LastResort = tofu in the rendered PDF)."""
    conv = md_to_html("正文引用。[^1]\n\n[^1]: 这是脚注内容。\n")
    assert "\u21a9" not in conv.html  # ↩ (missing outside Menlo)
    assert "\ufe0e" not in conv.html  # variation selector (missing everywhere)
    assert "footnote-backref" in conv.html
    assert "\u2191" in conv.html  # ↑ replacement, covered by all theme fonts


def test_robustness(tmp_path):
    broken = "# 标题\n\n- 未闭合列表\n\n| 表 |\n| --- |\n| a |\n\n```python\n未闭合\n"
    conv = md_to_html(broken)
    css, _ = theme_css("modern")
    out = tmp_path / "broken.pdf"
    render_pdf(build_document(conv), css, out)
    report = validate_pdf(out)
    assert report.pages >= 1
    assert report.checks[0].score > 0  # text selectable


def test_cli(tmp_path):
    src = tmp_path / "a.md"
    src.write_text("---\ntitle: CLI 测试\n---\n\n# 章节\n\n正文内容。\n", encoding="utf-8")
    out = tmp_path / "a.pdf"
    r = subprocess.run(
        [sys.executable, "-m", "imprint", str(src), "-o", str(out), "--report", str(tmp_path / "r.json")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr[-800:]
    assert out.exists()
    report = json.loads((tmp_path / "r.json").read_text(encoding="utf-8"))
    assert report["score"] >= 90
