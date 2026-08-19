"""MCP server: let an AI agent turn one sentence into a print-grade PDF.

Run with `imprint-mcp` (stdio transport), then point any MCP client
(Claude Code / Cursor / Copilot / DeepSeek Harness, ...) at it.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .converter import build_document, md_to_html
from .recommend import recommend_theme
from .render import render_pdf
from .theme import theme_css
from .themes import list_themes
from .validator import validate_pdf

mcp = FastMCP("imprint")


@mcp.tool()
def list_themes_tool() -> list[str]:
    """List the available print-grade themes (e.g. modern, academic, sepia)."""
    return list_themes()


@mcp.tool()
def render_markdown(markdown: str, theme: str = "", output: str = "") -> dict:
    """Render Markdown to a print-grade PDF and return the 0-100 quality report.

    Args:
        markdown: full Markdown source (YAML frontmatter with title/author/date/theme supported).
        theme: optional theme name; empty = automatic smart recommendation.
        output: optional PDF output path; empty = a temp file is used.
    """
    conv = md_to_html(markdown)
    meta = conv.meta
    theme_name = (theme or meta.get("theme") or "").strip().lower()
    note = ""
    if not theme_name:
        theme_name, note = recommend_theme(meta, conv.text)
    css, theme_data = theme_css(theme_name)
    html = build_document(conv)
    out = Path(output).expanduser() if output else Path(tempfile.mktemp(suffix=".pdf"))
    out.parent.mkdir(parents=True, exist_ok=True)
    pages = render_pdf(html, css, out)
    report = validate_pdf(
        out,
        toc_entries=[(i.text, i.href) for i in conv.toc],
        serif_hint=meta.get("theme-font-hint") or "Songti",
        theme_colors=theme_data["tokens"].get("color"),
    )
    return {
        "pdf": str(out),
        "pages": pages,
        "theme": theme_name,
        "theme_reason": note or "explicit",
        "score": report.score,
        "grade": report.grade,
        "report": report.to_dict(),
    }


@mcp.tool()
def validate_pdf_tool(pdf: str) -> dict:
    """Run the 0-100 print-quality report on an existing PDF."""
    report = validate_pdf(Path(pdf).expanduser())
    return {"score": report.score, "grade": report.grade, "report": report.to_dict()}


@mcp.tool()
def new_document_tool(template: str, output: str = "") -> str:
    """Scaffold a Markdown draft from a built-in template.

    Args:
        template: report | book | resume | techdoc | letter.
        output: optional output .md path; empty = <template>.md in cwd.
    """
    from importlib.resources import files

    tpl = template.removesuffix(".md")
    path = Path(str(files("imprint.templates").joinpath(f"{tpl}.md")))
    if not path.exists():
        raise ValueError(f"unknown template: {template}")
    target = Path(output).expanduser() if output else Path(f"{tpl}.md")
    target.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    return str(target)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
