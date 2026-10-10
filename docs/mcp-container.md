# MCP container and Glama submission

This image installs the checked-out source with the optional MCP dependency,
Pango and CJK fonts. It starts a **stdio** server as an unprivileged user;
it does not expose an HTTP port. It does not replace the existing PyPI release.

```bash
docker build -t imprint-mcp:source .
docker run --rm -i --network none --cap-drop ALL \
  --security-opt no-new-privileges imprint-mcp:source
```

The second command waits for a real MCP client over stdin/stdout. It is not an
interactive shell and does not print a readiness banner. For a client command,
use `docker` with arguments `run --rm -i --network none --cap-drop ALL
--security-opt no-new-privileges imprint-mcp:source`.

The registered tools are:

- `render_markdown`
- `list_themes_tool`
- `validate_pdf_tool`
- `new_document_tool`

Without a bind mount, output files remain in the container and disappear when
it exits. Mount only a dedicated output directory when persistence is needed;
never mount your home directory or credentials. Select a matching numeric user
ID for the host directory instead of making it world-writable.

## Verification and submission

The `MCP container` GitHub workflow builds this checkout on Linux, initializes
an official MCP client, lists all four tools, calls the theme and template
tools, checks the template file and non-root identity, renders a small PDF,
independently reads its pages and expected text, and validates that same PDF.
The score is required to be a numeric value in the declared 0–100 range and the
page count a positive integer; this is a serialization contract, not a minimum
quality threshold. A successful workflow
shows container functionality; it is not a Glama quality score, print-quality
certification, or an accessibility audit.

As checked on 2026-10-10, the [PR's latest listing feedback](https://github.com/punkpeye/awesome-mcp-servers/pull/12495)
asks for a Dockerfile directly in Glama. The account is not signed in and the
listing has not been submitted.
After the account owner completes the required sign-in or verification, use
the public repository URL and this Dockerfile in its submission form. Verify
the returned server page and checks before adding any score badge. A repository
`glama.json` file alone does not create a listing.

The official MCP Registry and Glama are separate directories. An active
official Registry entry cannot substitute for a Glama page when a PR reviewer
specifically requests Glama.

MCP is pinned to 1.30.0 in this candidate image and client. The base-image tag,
APT packages and other Python dependencies still follow available releases;
this is not a fully locked or bit-reproducible build. Do not describe it as such.
