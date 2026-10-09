# First success from a source checkout

Use Python 3.10+ and install the native prerequisites below first. From the repository root:

macOS/Linux:
```sh
python3 -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/python -m imprint --version
.venv/bin/python -m imprint examples/sample.md -o sample.pdf --report qa.json
```

Windows PowerShell:
```powershell
py -3.11 -m venv .venv
.venv/Scripts/python.exe -m pip install -e .
.venv/Scripts/python.exe -m imprint --version
.venv/Scripts/python.exe -m imprint examples/sample.md -o sample.pdf --report qa.json
```

This checkout reports `imprint 0.14.0`. After installing dependencies, this bundled Markdown sample renders locally without API keys or paid services. Open `sample.pdf` and inspect the evidence in `qa.json`. Font availability can change pagination and score.

| Platform | Native prerequisites | Notes |
|---|---|---|
| macOS | Homebrew Pango (`brew install pango`) | Expose the Homebrew library directory if loading fails: normally `/opt/homebrew/lib` on Apple Silicon or `/usr/local/lib` on Intel. |
| Debian/Ubuntu | `libpango-1.0-0`, `libpangoft2-1.0-0`, `fonts-noto-cjk` | Other distributions use equivalent Pango/GLib packages. |
| Windows | GTK3/Pango matching Python architecture; DLL directory on PATH | GTK2 is too old. Follow the chosen WeasyPrint version's installation guide. |

Install an appropriate licensed CJK font for Chinese documents. Native libraries and fonts are outside pip/npm. See the [WeasyPrint installation reference](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html). The repository CI matrix targets macOS, Ubuntu and Windows on Python 3.10–3.12; a matrix definition alone does not mean every current job passed.

## Version boundaries

Python runtime, project, npm wrapper and MCP source metadata are aligned to 0.14.0. Check PyPI, npm and GitHub Release independently before pinning an installation; matching version labels alone do not guarantee matching artifact contents. The npm package is `imprint-pdf`; `imprint` is the installed command name. `npx imprint` can select a different package.

`node npm/cli.js --version` reports this wrapper's version without installation, not the version of the Python engine selected from PATH. The wrapper may reuse an existing engine or install a registry package; use an explicit virtual environment for reproducible rendering. `python -m pytest tests/test_release_metadata.py -q` checks local metadata without registry requests.

## Report limits

The 0–100 report is a heuristic over implemented checks: 100 means no deductions, not print-house certification. Rendering requests WeasyPrint's PDF/UA-1 variant, but the `pdf_ua` check only inspects the catalog MarkInfo flag. It does not establish reading order, image descriptions, screen-reader usability or full PDF/UA conformance. Contrast checks compare theme tokens, not every rendered element. Use a dedicated accessibility validator and a human print proof for release work.

The v0.14.0 GitHub source release and npm package are published. PyPI already contained version 0.14.0 before this source release; this work did not replace its wheel, so verify the registry artifact contents separately when exact source parity matters. The checkout sample is not included in the installed wheel. For registry use, create your own Markdown input or run `imprint --new report -o report.md`, then `imprint report.md -o report.pdf --report qa.json`. Source-only documentation corrections are not promised by a registry installation.
