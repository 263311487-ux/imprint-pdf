# Contributing

Thanks for considering contributing to Imprint! This is an early project, so
even small PRs (a theme tweak, a docs fix, a quality-check edge case) are
highly welcome.

## Development setup

```bash
python -m venv .venv
.venv/bin/pip install -e ".[charts,mcp]" pytest
.venv/bin/python -m pytest tests/            # must be green
.venv/bin/python -m imprint examples/sample.md  # expect 100/100 A+
```

WeasyPrint needs Pango on your system:

- macOS: `brew install pango`
- Debian/Ubuntu: `sudo apt install libpango-1.0-0 libpangoft2-1.0-0`
- Windows: install the [GTK3 runtime](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer)

## Quality gate

- Every change keeps `pytest` green (CI runs macOS/Linux/Windows × Python 3.10–3.12).
- Every shipped example PDF must score **100/100 A+** on the built-in report.
- A theme change must pass the full 22-theme regression (`tests` renders all themes).
- Prefer evidence over vibes: when you fix a quality-check edge case, add a test.

## Adding a theme

1. Add `imprint/themes/<name>.json` following the DTCG-style schema in an existing theme.
2. Verify contrast: render a sample and check the `contrast` check is 5/5.
3. Add the keyword signals in `imprint/recommend.py` if the theme has a distinctive mood.
4. Regenerate a gallery image (`examples/qa/<name>-01.png`) and add it to `README.md`.

## Code style

- Keep changes minimal and consistent with the existing style.
- No new dependencies unless there is a real reason; ask first.
