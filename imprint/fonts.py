"""Theme font availability check via fontconfig (fc-match)."""

from __future__ import annotations

import re
import shutil
import subprocess
from typing import Any

_FAMILY_SPLIT = re.compile(r'"[^"]*"|[^,"]+')


def parse_families(stack: str) -> list[str]:
    """Split a CSS font stack like '"Songti SC", serif' into family names."""
    names = []
    for m in _FAMILY_SPLIT.findall(stack or ""):
        name = m.strip().strip('"')
        if name and name not in ("serif", "sans-serif", "monospace", "cursive"):
            names.append(name)
    return names


def _fc_match(family: str) -> str:
    try:
        out = subprocess.run(
            ["fc-match", family], capture_output=True, text=True, timeout=10
        )
        return (out.stdout or "").strip()
    except Exception:
        return ""


def missing_font_slots(theme: dict[str, Any]) -> list[str]:
    """Return labels of font slots whose whole stack is unavailable locally.

    A slot is reported missing only when *none* of its declared families can
    be resolved by fontconfig, meaning text will fall back to a system font.
    Returns [] when fontconfig is not installed (cannot check, not an error).
    """
    if shutil.which("fc-match") is None:
        return []
    typo = theme.get("tokens", {}).get("typography", {})
    slots = {
        "正文（衬线）": typo.get("font-serif", ""),
        "标题（无衬线）": typo.get("font-sans", ""),
        "代码（等宽）": typo.get("font-mono", ""),
    }
    missing = []
    for label, stack in slots.items():
        families = parse_families(stack)
        if not families:
            continue
        if not any(f in _fc_match(f) for f in families):
            missing.append(label)
    return missing
