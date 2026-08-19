import asyncio
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

mcp = pytest.importorskip("mcp")


def test_mcp_tools_registered():
    from imprint.mcp_server import mcp

    names = {t.name for t in mcp._tool_manager.list_tools()}
    assert {"render_markdown", "list_themes_tool", "validate_pdf_tool", "new_document_tool"} <= names


def test_mcp_render_tool(tmp_path):
    from imprint.mcp_server import render_markdown

    md = "---\ntitle: MCP 测试\n---\n\n# 章节\n\n这是通过 MCP 工具生成的文档。\n"
    out = tmp_path / "mcp.pdf"
    res = render_markdown(md, theme="modern", output=str(out))
    assert out.exists()
    assert res["pages"] >= 1
    assert res["score"] >= 95, res["report"]
    assert res["pdf"] == str(out)


def test_mcp_stdio_roundtrip():
    """A real session over stdio using the official MCP client."""
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    async def run():
        # mcp's stdio client whitelists the child env (drops e.g.
        # DYLD_FALLBACK_LIBRARY_PATH on macOS); inherit everything so the
        # child can load pango/glib the same way the parent does.
        env = {**__import__("os").environ}
        params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "imprint.mcp_server"],
            cwd=str(ROOT),
            env=env,
        )
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await session.list_tools()
                names = [t.name for t in tools.tools]
                assert "render_markdown" in names
                res = await session.call_tool(
                    "list_themes_tool", {}
                )
                text = " ".join(
                    c.text if hasattr(c, "text") else str(c) for c in res.content
                )
                assert "modern" in text

    asyncio.run(asyncio.wait_for(run(), timeout=60))
