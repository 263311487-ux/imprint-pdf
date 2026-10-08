# imprint-pdf

**AI-native, print-grade Chinese PDF generator.** Markdown in, publisher-quality PDF out — with a built-in 0-100 print-quality report.

One command, after platform dependencies:

```bash
npx imprint-pdf 论文.md
npx imprint-pdf 论文.md --theme academic --out 论文.pdf
```

The first run auto-installs the Python engine (PyPI → GitHub fallback), then everything runs locally. The published package name is `imprint-pdf`; `imprint` is its CLI binary, not the npm package name. 24 built-in themes (academic / modern / minimal / ink / traditional ...), smart theme auto-recommendation, a request for tagged PDF/UA-1 output (not a conformance certification), and a rigorous print-quality validator (page balance, widow/orphan control, CJK typography, ink coverage, font embedding).

```bash
npx imprint-pdf --list-themes     # all 24 themes
npx imprint-pdf --new report      # scaffold from a template
npx imprint-pdf report.md --report qa.json   # export quality report
```

Showcase: https://263311487-ux.github.io/imprint-pdf/
Full docs: https://github.com/263311487-ux/imprint-pdf
MIT License.

## First success, offline

The npm wrapper delegates to the Python engine. For a no-network smoke test from a checkout, run `node cli.js --version`; it must print `imprint 0.14.0`. A real PDF additionally needs Python 3.10+, the Python dependencies from `pyproject.toml`, and WeasyPrint's native Pango/GLib stack. The wrapper may install from a registry on first use; use `python3 -m imprint` when dependencies are already installed.

On macOS install Pango with Homebrew; on Debian/Ubuntu install `libpango-1.0-0`, `libpangoft2-1.0-0`, and a CJK font package; on Windows install a current GTK3 runtime. These native libraries are outside npm and are not installed by this repository.
