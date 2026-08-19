"""DTCG-style design tokens -> print-grade CSS for WeasyPrint."""

from __future__ import annotations

from .themes import load_theme


CSS_TEMPLATE = """
@page {{
  size: A4;
  margin: {margin};
  @top-left {{
    content: string(booktitle);
    font-family: {sans};
    font-size: 7.5pt;
    color: {muted};
    letter-spacing: 0.3em;
  }}
  @top-right {{
    content: string(chapter);
    font-family: {sans};
    font-size: 7.5pt;
    color: {muted};
    letter-spacing: 0.12em;
  }}
  @bottom-center {{
    content: "· " counter(page) " ·";
    font-family: {sans};
    font-size: 8pt;
    color: {muted};
  }}
}}

@page cover {{
  margin: 0;
  @top-left {{ content: none; }}
  @top-right {{ content: none; }}
  @bottom-center {{ content: none; }}
}}

@page toc {{
  @top-left {{ content: none; }}
  @top-right {{ content: none; }}
}}

html {{
  font-size: 10.5pt;
}}

body {{
  font-family: {serif};
  font-size: {body};
  line-height: {line_height};
  color: {ink};
  background: {paper};
  text-align: justify;
  letter-spacing: 0.02em;
}}

/* ---------- cover ---------- */
.cover {{
  page: cover;
  page-break-after: always;
  height: 29.7cm;
  box-sizing: border-box;
  position: relative;
  text-align: center;
  padding-top: 8.2cm;
}}
.cover h1, .cover h2, .cover p {{
  page-break-before: auto;
  break-before: auto;
  string-set: none;
}}
.cover .brand {{
  font-family: {sans};
  font-size: 8pt;
  letter-spacing: 0.55em;
  color: {muted};
  margin: 0 0 1.9em;
}}
.cover .title {{
  font-family: {sans};
  font-size: 34pt;
  font-weight: 700;
  color: {ink};
  letter-spacing: 0.16em;
  margin: 0 0 0.25em;
}}
.cover .subtitle {{
  font-size: {h2};
  color: {muted};
  margin: 0;
}}
.cover .rule {{
  width: 4.6cm;
  border-top: 1pt solid {accent};
  margin: 1.15em auto 1.15em;
  position: relative;
}}
.cover .rule::before {{
  content: "";
  display: block;
  width: 5pt;
  height: 5pt;
  background: {accent};
  transform: rotate(45deg);
  margin: -3pt auto 0;
}}
.cover .meta {{
  position: absolute;
  bottom: 2.6cm;
  left: 0;
  right: 0;
  font-size: {small};
  color: {muted};
  line-height: 2.1;
  letter-spacing: 0.12em;
}}
.cover .meta .author {{
  font-family: {sans};
  font-weight: 600;
  color: {ink};
}}

/* ---------- TOC ---------- */
.toc-page {{
  page: toc;
  page-break-after: always;
}}
.toc-page h2 {{
  text-align: center;
  font-size: 16pt;
  letter-spacing: 0.7em;
  color: {ink};
  margin: 0 0 2.4em;
  text-indent: 0.7em;
}}
.toc-page h2::after {{
  content: "";
  display: block;
  width: 3cm;
  border-bottom: 1pt solid {accent};
  margin: 0.9em auto 0;
}}
.toc-list {{
  list-style: none;
  margin: 0;
  padding: 0;
}}
.toc-list li {{
  margin: 1.05em 0;
  line-height: 1.5;
}}
.toc-list a {{
  text-decoration: none;
  color: {ink};
}}
.toc-list li.l1 a {{
  font-family: {sans};
  font-weight: 600;
  font-size: 1.06em;
}}
.toc-list li.l2 {{
  padding-left: 1.8em;
}}
.toc-list li.l3 {{
  padding-left: 3.6em;
  font-size: 0.92em;
  color: {muted};
}}
.toc-list li a::after {{
  content: leader(". ") target-counter(attr(href), page);
  color: {muted};
  font-weight: 400;
}}

/* ---------- headings ---------- */
h1, h2, h3, h4 {{
  font-family: {sans};
  color: {ink};
  text-align: left;
  break-after: avoid;
  orphans: 3;
  widows: 3;
}}
h1 {{
  font-size: {h1};
  letter-spacing: 0.09em;
  margin: 0 0 1.3em;
  padding-bottom: 0.5em;
  border-bottom: 0.9pt solid {line};
  page-break-before: always;
  string-set: chapter content();
}}
h1::after {{
  content: "";
  display: block;
  width: 6.5em;
  max-width: 38%;
  border-bottom: 2.4pt solid {accent};
  margin-top: 0.42em;
}}
h1.first {{ page-break-before: auto; }}
h2 {{
  font-size: {h2};
  letter-spacing: 0.05em;
  margin: 1.7em 0 0.8em;
  padding: 0.1em 0 0.1em 0.7em;
  border-left: 3.2pt solid {accent};
}}
h3 {{
  font-size: {h3};
  letter-spacing: 0.03em;
  margin: 1.3em 0 0.55em;
}}
h4 {{
  font-size: {body};
  font-weight: 700;
  margin: 1em 0 0.4em;
}}

/* ---------- paragraphs ---------- */
p {{
  margin: 0;
  text-indent: {para_indent};
  text-align: justify;
}}
p.first, p.noindent {{
  text-indent: 0;
}}
li p, td p, th p, blockquote p {{
  text-indent: 0;
}}

p[lang="en"], li[lang="en"], div[lang="en"] {{
  text-indent: 0;
  hyphens: auto;
  letter-spacing: 0;
}}

/* ---------- lists ---------- */
ul, ol {{
  margin: 0.5em 0 1em;
  padding-left: 1.9em;
}}
li {{
  margin: 0.28em 0;
  break-inside: avoid;
}}
ul.task-list {{ list-style: none; padding-left: 0.4em; }}

/* ---------- blockquote ---------- */
blockquote {{
  margin: 1.1em 0 1.4em;
  padding: 0.75em 1.2em 0.75em 1.5em;
  border-left: 2.4pt solid {accent};
  background: {accent_soft};
  position: relative;
  break-inside: avoid;
}}
blockquote::before {{
  content: "\\201C";
  position: absolute;
  top: -0.1em;
  left: 0.18em;
  font-family: {serif};
  font-size: 30pt;
  color: {accent};
  opacity: 0.28;
  line-height: 1;
}}
blockquote p {{ margin: 0.2em 0; }}


/* ---------- GitHub-style alerts ---------- */
blockquote.alert {{
  break-inside: avoid;
}}
blockquote.alert::before {{
  content: attr(data-label);
  display: block;
  font-family: {sans};
  font-weight: 700;
  font-size: 8pt;
  letter-spacing: 0.3em;
  margin: 0 0 0.55em;
  opacity: 1;
}}
blockquote.alert p {{
  margin: 0.2em 0;
}}
blockquote.alert-note {{
  border-left-color: #0969da;
  background: #f2f8ff;
}}
blockquote.alert-note::before {{ color: #0969da; }}
blockquote.alert-tip {{
  border-left-color: #1a7f37;
  background: #f1faf3;
}}
blockquote.alert-tip::before {{ color: #1a7f37; }}
blockquote.alert-important {{
  border-left-color: #8250df;
  background: #f8f4ff;
}}
blockquote.alert-important::before {{ color: #8250df; }}
blockquote.alert-warning {{
  border-left-color: #9a6700;
  background: #fffbf0;
}}
blockquote.alert-warning::before {{ color: #9a6700; }}
blockquote.alert-caution {{
  border-left-color: #cf222e;
  background: #fff5f4;
}}
blockquote.alert-caution::before {{ color: #cf222e; }}

/* ---------- table (booktabs style) ---------- */
table {{
  width: 100%;
  border-collapse: collapse;
  margin: 1em 0 1.5em;
  font-size: {body};
}}
thead {{
  display: table-header-group;
}}
thead th {{
  background: transparent;
  color: {ink};
  font-family: {sans};
  font-weight: 600;
  font-size: 0.9em;
  border: none;
  border-top: 1.3pt solid {ink};
  border-bottom: 0.7pt solid {ink};
  padding: 5pt 8pt;
  text-align: left;
}}
td {{
  border: none;
  border-bottom: 0.35pt solid {line};
  padding: 4.6pt 8pt;
  vertical-align: top;
}}
tbody tr:last-child td {{
  border-bottom: 1.3pt solid {ink};
}}
tr {{ break-inside: avoid; }}

/* ---------- code ---------- */
pre {{
  background: {code_bg};
  border: 0.5pt solid {line};
  border-radius: {code_radius};
  padding: 10pt 12pt;
  font-family: {mono};
  font-size: 8.8pt;
  line-height: 1.55;
  white-space: pre-wrap;
  break-inside: avoid;
  margin: 1em 0 1.4em;
}}
pre.code-block::before {{
  content: attr(data-lang);
  display: block;
  font-family: {sans};
  font-size: 6.6pt;
  letter-spacing: 0.3em;
  color: {muted};
  margin: -4pt 0 8pt;
  padding-bottom: 7pt;
  border-bottom: 0.4pt solid {line};
}}
code {{
  font-family: {mono};
  font-size: 0.92em;
}}
p code, li code, td code {{
  background: {code_bg};
  padding: 0.5pt 3pt;
  border-radius: 2pt;
}}
.highlight pre {{ background: transparent; border: none; padding: 0; }}

/* ---------- images ---------- */
img {{
  max-width: 100%;
  page-break-inside: avoid;
}}
p.figure, p > img {{ text-align: center; }}
p.figure img {{ margin: 0.6em 0 0.2em; }}
figcaption {{
  font-size: {small};
  color: {muted};
  text-align: center;
  margin: 0.4em 0 1.2em;
}}



/* ---------- math ---------- */
img.math-inline {{
  height: 1.2em;
  vertical-align: middle;
}}
.math-display {{
  text-align: center;
  margin: 1em 0 1.4em;
  break-inside: avoid;
}}
.math-display img {{
  max-width: 100%;
  height: auto;
}}

/* ---------- mermaid figures ---------- */
.mermaid-figure {{
  margin: 1.2em 0 1.6em;
  text-align: center;
  break-inside: avoid;
  page-break-inside: avoid;
}}
.mermaid-figure img {{
  max-width: 100%;
  height: auto;
}}

/* ---------- footnotes ---------- */
.footnotes {{
  font-size: 8pt;
  line-height: 1.6;
  color: {ink};
  border-top: 0.4pt solid {line};
  margin-top: 1.4em;
  padding-top: 0.6em;
}}
.footnotes hr {{ display: none; }}
sup {{ font-size: 0.72em; }}

/* ---------- misc ---------- */
a {{ color: {ink}; text-decoration: none; }}
hr {{
  border: none;
  border-top: 0.5pt solid {line};
  margin: 1.4em 0;
}}
strong {{ font-weight: 700; }}
mark {{
  background: {accent_soft};
  padding: 0 2pt;
}}

/* ---------- code highlight colors (Pygments) ---------- */
.highlight .c, .highlight .c1 {{ color: #6a737d; font-style: italic; }}
.highlight .k, .highlight .kd, .highlight .kn, .highlight .kr {{ color: #d73a49; font-weight: 600; }}
.highlight .s, .highlight .s1, .highlight .s2 {{ color: #032f62; }}
.highlight .nf, .highlight .fm {{ color: #6f42c1; }}
.highlight .nb, .highlight .bp, .highlight .mi, .highlight .mf, .highlight .mh {{ color: #005cc5; }}
.highlight .nc, .highlight .nd {{ color: #e36209; }}
.highlight .o {{ color: #24292e; }}
"""


def tokens_to_css(tokens: dict, theme: dict) -> str:
    c = tokens["color"]
    t = tokens["typography"]
    s = tokens["spacing"]
    d = tokens["decoration"]
    t.setdefault("font-serif-alt", t["font-serif"])
    return CSS_TEMPLATE.format(
        margin=s["page-margin"],
        sans=t["font-sans"],
        serif=t["font-serif"],
        serif_alt=t["font-serif-alt"],
        mono=t["font-mono"],
        body=t["size-body"],
        small=t["size-small"],
        h1=t["size-h1"],
        h2=t["size-h2"],
        h3=t["size-h3"],
        line_height=t["line-height"],
        ink=c["ink"],
        paper=c["paper"],
        accent=c["accent"],
        accent_soft=c.get("accent-soft", "#f2f2f2"),
        accent_soft_half=c.get("accent-soft", "#fafafa"),
        muted=c["muted"],
        line=c["line"],
        code_bg=c["code-bg"],
        table_head=c["table-head"],
        para_indent=s["para-indent"],
        heading_gap=s["heading-gap"],
        h1_rule=d["h1-rule"],
        quote_bar=d["quote-bar"],
        code_radius=d["code-radius"],
    )


def theme_css(name: str, extra_dir: str | None = None) -> tuple[str, dict]:
    theme = load_theme(name, extra_dir)
    css = tokens_to_css(theme["tokens"], theme)
    return css, theme
