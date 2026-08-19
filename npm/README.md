# imprint-pdf

**AI-native, print-grade Chinese PDF generator.** Markdown in, publisher-quality PDF out — with a built-in 0-100 print-quality report.

One command, zero config:

```bash
npx imprint-pdf 论文.md
npx imprint-pdf 论文.md --theme academic --out 论文.pdf
```

The first run auto-installs the Python engine (PyPI → GitHub fallback), then everything runs locally. 24 built-in themes (academic / modern / minimal / ink / traditional ...), smart theme auto-recommendation, PDF/UA accessibility, and a rigorous print-quality validator (page balance, widow/orphan control, CJK typography, ink coverage, font embedding).

```bash
npx imprint-pdf --list-themes     # all 24 themes
npx imprint-pdf --new report      # scaffold from a template
npx imprint-pdf report.md --report qa.json   # export quality report
```

Showcase: https://263311487-ux.github.io/imprint-pdf/
Full docs: https://github.com/263311487-ux/imprint-pdf
MIT License.
