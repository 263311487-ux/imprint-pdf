"""Built-in theme registry."""

from __future__ import annotations

import json
from importlib.resources import files
from pathlib import Path


def _builtin_themes() -> tuple[str, ...]:
    return tuple(
        sorted(
            p.name.removesuffix(".json")
            for p in files("imprint.themes").iterdir()
            if p.name.endswith(".json")
        )
    )


BUILTIN_THEMES = _builtin_themes()


def load_theme(name: str, extra_dir: str | None = None) -> dict:
    """Load a DTCG-style theme tokens file from builtins or an extra directory."""
    name = name.removesuffix(".json")
    candidates: list[Path] = []
    if extra_dir:
        candidates.append(Path(extra_dir) / f"{name}.json")
    candidates.append(Path(str(files("imprint.themes").joinpath(f"{name}.json"))))
    for path in candidates:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    raise FileNotFoundError(f"theme not found: {name} (available: {', '.join(_builtin_themes())})")


def list_themes(extra_dir: str | None = None) -> list[str]:
    names = list(_builtin_themes())
    if extra_dir:
        for p in sorted(Path(extra_dir).glob("*.json")):
            if p.stem not in names:
                names.append(p.stem)
    return names
