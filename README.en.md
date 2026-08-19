# Imprint

> **Markdown in, publisher-grade PDF out — with a built-in 0–100 print-quality report.**

Imprint is an AI-native, print-grade Chinese PDF generator. It treats Markdown as the draft and the PDF as the finished product, following publishing standards: serif body text, sans headings, 2-em first-line indents, kinsoku punctuation rules, exact TOC page numbers, repeating table headers across pages, and code blocks that never split mid-line. After every render it scores the PDF **0–100** and shows evidence for every check.

[简体中文](README.md) · [Live showcase](https://263311487-ux.github.io/imprint-pdf/)

<p align="center">
  <img alt="PyPI" src="https://img.shields.io/pypi/v/imprint-pdf.svg">
  <img alt="npm" src="https://img.shields.io/npm/v/imprint-pdf.svg">
  <img alt="Python" src="https://img.shields.io/pypi/pyversions/imprint-pdf.svg">
  <img alt="License" src="https://img.shields.io/pypi/l/imprint-pdf.svg">
  <img alt="Downloads" src="https://img.shields.io/pypi/dm/imprint-pdf.svg">
  <img alt="CI" src="https://github.com/263311487-ux/imprint-pdf/actions/workflows/ci.yml/badge.svg">
  <img alt="Stars" src="https://img.shields.io/github/stars/263311487-ux/imprint-pdf">
</p>

## Quick start (zero config)

```bash
# One command — auto-installs the engine (cross-platform)
npx imprint-pdf paper.md

# or via pip (GitHub source until the PyPI release lands)
pip install "imprint-pdf @ git+https://github.com/263311487-ux/imprint-pdf.git"
imprint paper.md

# Common commands
npx imprint-pdf --new report        # scaffold from a template
npx imprint-pdf --list-themes       # all 24 themes
npx imprint-pdf paper.md --theme academic --out paper.pdf
```

![Cover](examples/qa/sample-01.png)

![TOC](examples/qa/sample-02.png)

![Body](examples/qa/sample-04.png)

![Alerts](examples/qa/alerts-03.png)

![Mermaid chart](examples/qa/charts-03.png)

## Why Imprint

Most Markdown→PDF pipelines (pandoc defaults, md2pdf, browser print) just "pour text into pages". Imprint is different in three ways:

- **Print-grade Chinese typography** — kinsoku line-breaking rules, 2-em first-line indents, CJK/Latin spacing, widow & orphan control
- **Themes as design systems** — every theme is a set of DTCG design tokens (palette / type pairing / spacing / decoration); switching themes is one argument
- **A print-quality report on every PDF** — 14 automated checks, scored 0–100, with evidence for each one

## Quick start

```bash
pip install "imprint-pdf @ git+https://github.com/263311487-ux/imprint-pdf.git"
# charts support (optional)
pip install "imprint-pdf[charts] @ git+https://github.com/263311487-ux/imprint-pdf.git"
# MCP server (optional): an agent turns one sentence into a report
pip install "imprint-pdf[mcp] @ git+https://github.com/263311487-ux/imprint-pdf.git"

imprint paper.md -o paper.pdf
imprint paper.md --theme sepia --compress
# scaffold from a starter template (report/book/resume/techdoc/letter/paper/gongwen/ieee)
imprint --new report -o my_report.md
# start the MCP server (stdio) for Claude Code / Cursor / DeepSeek Harness, ...
imprint-mcp
```

Every run ends with a quality report:

```
印刷级质检报告
==============================================
 ✓ 文本可选              15.0/15.0   平均每页 722 字符
 ✓ 字体子集嵌入            15.0/15.0   5/5 字体已嵌入
 ✓ 元数据完整              3.0/3.0    标题「印记」
 ✓ 标点避头尾             15.0/15.0   0 违规
 ✓ 孤行寡行               9.0/9.0    0 处
 ✓ 目录页码              15.0/15.0   核对 15 条
 ✓ 页码存在               2.0/2.0    8/9 页含页码
 ✓ PDF/UA 标签          3.0/3.0    Tagged PDF
 ✓ 主题字体生效             3.0/3.0    命中 songti
 ✓ 主题对比度              5.0/5.0    正文 17.0:1 …
 ✓ 缺字检测               5.0/5.0    无缺字回退
 ✓ 内容溢出               5.0/5.0    无内容越界
 ✓ 图片清晰度              5.0/5.0    全部达标
 ----------------------------------------------
 总分 100.0/100 · 等级 A+ · 9 页
```

## Features

- **Cover + TOC** — frontmatter `title / author / date` builds a cover; headings become a clickable TOC with page numbers that actually match
- **Smart theming** — pick a theme explicitly, or let Imprint read the document and recommend one (with the reason why); 24 themes, including a dark one
- **Theme gallery** — modern / academic / nord / sepia / newspaper / catppuccin / mono / jade / coffee / ocean / lavender / rose / pine / wine / graphite / midnight (dark) / coral / amber / mint / sand / minimal / ink (thread-bound book, rice paper + seal red) / gongwen (red-header official document) / ieee (English two-column paper); custom themes are a single JSON file
- **GitHub-style alerts** — `> [!NOTE]` / `[!TIP]` / `[!WARNING]` / `[!IMPORTANT]` / `[!CAUTION]` render as print-grade callout cards
- **Mermaid diagrams** — ` ```mermaid ` fences render to vector images (Chinese labels included); graceful code-block fallback when the engine is missing
- **Math** — `$inline$` / `$$block$$` become vector SVG via matplotlib mathtext; no LaTeX or math fonts required
- **Starter templates** — `imprint --new report|book|resume|techdoc|letter|paper|gongwen|ieee` (the `paper` template renders a **two-column academic paper**; `ieee` renders an **IEEE-style English paper**; `gongwen` renders a **GB/T 9704 Chinese government document** with red letterhead, document number, red rule, and right-aligned signature)
- **Two-column academic layout** — `layout: two-column` in frontmatter; headings never orphan, tables never split mid-row, inline math never breaks a line
- **Red-header official documents** — `layout: gongwen` in frontmatter; no cover/TOC, GB/T 9704 red letterhead with ★ rule, FangSong body, right-aligned seal block
- **English papers** — `lang: en` in frontmatter sets the document language tag for PDF/UA; `theme-font-hint` accepts multi-word font names like "Times New Roman"
- **Image compression** — `--compress` downscales oversized images and re-encodes (measured 11.7 MB → 1.4 MB)
- **Font health check** — warns before rendering if a theme's font slot is missing on this machine
- **Chinese typography rules** — kinsoku, first-line indent, CJK/Latin spacing, hyphenation for English paragraphs
- **Cross-page tables** — header row repeats, rows never split
- **Code highlighting** — Pygments colors; blocks move to a fresh page instead of splitting
- **Missing-glyph detection** — scans for LastResort/notdef fallback (tofu boxes) so symbols like footnote arrows never silently break
- **PDF/UA** — tagged, accessible PDF by default
- **WCAG contrast** — every theme passes the print checks (body ≥ 7:1, small text ≥ 4.5:1, decoration ≥ 3:1)
- **AI-native** — one command from the CLI; a built-in MCP server (`imprint-mcp`) lets an agent produce a report from a sentence (tools: render_markdown / list_themes / validate_pdf / new_document)

## Quality report (14 checks, 100 points)

| check | points | what it verifies |
|---|---|---|
| text_selectable | 15 | text is text, not a screenshot |
| fonts_embedded | 15 | font subsets are embedded |
| punctuation | 15 | zero kinsoku violations |
| toc | 15 | TOC page numbers match reality |
| widows_orphans | 9 | no heading stranded at page bottom |
| metadata | 3 | PDF has a title |
| theme_fonts | 3 | the theme's fonts actually got used |
| pdf_ua | 3 | tagged, accessible PDF |
| page_numbers | 2 | page numbers present |
| contrast | 5 | WCAG contrast in print |
| glyph_coverage | 5 | no missing-glyph fallback (tofu) |
| overflow | 5 | no content past the page edge |
| image_dpi | 5 | embedded images ≥ 150 DPI |

## Comparison

| | pandoc default | browser print | Imprint |
|---|---|---|---|
| Chinese print-grade | weak | weak | **spec-compliant** |
| design-system themes | none | none | **DTCG tokens** |
| 0–100 quality report | none | none | **built-in** |
| math | plugin | none | **vector, embedded** |
| starter templates | none | none | **8 built-in** |
| WCAG contrast | none | none | **built-in** |
| PDF/UA accessible | manual | none | **default** |

## Development

```bash
python -m venv .venv && .venv/bin/pip install -e ".[charts]" pytest
.venv/bin/python -m pytest tests/
.venv/bin/python -m imprint examples/sample.md   # expect 100/100 A+
```

CI runs pytest on macOS / Linux / Windows × Python 3.10–3.12.

## Roadmap

- [x] 24 themes · 8 templates · two-column papers · red-header docs · IEEE English papers
- [x] npm distribution (`npx imprint-pdf`)
- [ ] PyPI release (pip install imprint-pdf)
- [ ] More templates: medical records, contracts

## License

MIT
