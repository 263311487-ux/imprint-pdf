# Contributing to imprint-pdf (印记)

## Ways to contribute

- **Typography bugs**: incorrect punctuation kinsoku, broken CJK line-break, table header not repeating — include the Markdown source and the quality report output.
- **New themes**: a theme is a JSON token file in `imprint/themes/`. See existing themes for the schema (color palette, font stack, spacing scale).
- **Quality report checks**: new checks in the 0–100 report need evidence (what does a pass mean, how is it measured?).
- **MCP tool improvements**: new tools or parameters for the `imprint-mcp` server.
- **Platform support**: test results on Windows/macOS/Linux with specific GTK/Pango versions.

## Development setup

```bash
git clone https://github.com/263311487-ux/imprint-pdf.git
cd imprint-pdf
pip install -e ".[charts,mcp]" pytest
python -m pytest tests/ -q
python -m imprint examples/sample.md --no-validate
```

Requirements: Python 3.10+, WeasyPrint system libs (Pango/GLib — see first-success guide).

## Pull request checklist

- [ ] `python -m pytest tests/ -q` passes
- [ ] `python -m imprint examples/sample.md --no-validate` completes without error
- [ ] New theme: at least one QA screenshot added to `docs/qa/`
- [ ] New quality check: documented in the commit message with measurement method
- [ ] No new optional dependencies without justification in `pyproject.toml`

## Theme authoring

1. Copy an existing theme JSON from `imprint/themes/`
2. Adjust tokens (colors in OKLCH or HEX, font stack, spacing)
3. Run `python -m imprint examples/sample.md --theme your-theme` and verify output
4. Add a screenshot to `docs/qa/` named `your-theme-01.png`
5. List the theme in `README.md`'s theme gallery section

## Quality report contributions

Each check in the 0–100 report needs:
- A name and point value
- A measurement method (what to check in the PDF)
- A pass/fail threshold
- At least one test case in `tests/`
