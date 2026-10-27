# Security Policy

## Supported versions

| Version | Supported |
|---|---|
| 0.14.x (latest) | ✅ |
| < 0.14 | ❌ |

## Reporting a vulnerability

1. **Do not** open a public issue.
2. Email: 263311487@qq.com with description, reproduction steps, and severity.
3. Response within 72 hours.

## Scope

- Markdown parsing and PDF rendering pipeline
- MCP server input validation (tool argument sanitization)
- The demo server (`demo_server/render_server.py`) — note: not for production use

## Notes

- imprint-pdf renders Markdown to PDF locally. The online demo sends Markdown to a hosted server — **do not upload sensitive content to the demo**.
- The MCP server runs locally (stdio transport) and does not make outbound requests beyond what WeasyPrint needs for fonts/images referenced in your Markdown.
