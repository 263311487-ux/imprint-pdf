# Why a 0-100 print-quality gate?

Most "Markdown → PDF" tools stop at "the PDF rendered". Imprint stops one step later: **it re-opens the PDF it just made and grades itself like a print inspector would.**

## What the validator actually checks

| Check | Why it matters |
|---|---|
| Page balance & widow/orphan control | A report with one line stranded at the bottom of a page looks broken to a human, even if every pixel is technically there |
| CJK punctuation avoidance (标点避头尾) | Chinese punctuation at the start of a line is a typographic error readers notice instantly |
| Font embedding & coverage | Text that silently falls back to a wrong font (or renders as tofu ▯) defeats the purpose of a PDF |
| Exact TOC page numbers (read from PDF bookmarks) | A table of contents that lies is worse than no TOC |
| Contrast (WCAG) | Theme tokens are pre-checked, but the gate re-verifies against the actual rendered PDF |
| Image resolution ≥150 DPI | Screen-only images look fine on screen and blurry in print |
| Content overflow | Tables/code that clip at the page edge |
| PDF/UA accessibility labels | Screen readers can read the document |
| Ink coverage / line hyphens (CJK) | Aesthetic evenness professional typesetters care about |

## Why a *score* and not just pass/fail

- **For humans**: a single number tells you "this is ready to send" vs "keep fixing". 100/100 is a hard, achievable bar (Imprint's own test corpus runs 100/100).
- **For AI agents**: the MCP server returns the score + a list of failed checks with machine-readable keys, so an agent can iterate: render → read report → fix → re-render. This turns document generation into a *closed loop* instead of a blind one-shot.
- **For CI**: `imprint doc.md --report qa.json` gives CI a quality gate. Same philosophy as linting for code, but for documents.

## The philosophy

LaTeX gives you control and no quality signal. Word gives you neither. Imprint's bet: **the tool should be opinionated about quality, and it should prove it with evidence** — not vibes.

Each deduction in the report carries the *key* of the failed check and the *evidence* (e.g. "line 3 of page 2 is an orphan: `widow-orphan: line=3,page=2`"). You can see exactly what to fix, and fix it in the Markdown, not in the layout engine.
