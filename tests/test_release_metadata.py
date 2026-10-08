import json
import re
import shutil
import subprocess

import pytest
from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_release_metadata_is_consistent_across_python_npm_and_mcp():
    py_version = re.search(r'__version__\s*=\s*"([^"]+)"', (ROOT / "imprint/__init__.py").read_text()).group(1)
    project = re.search(r'^version\s*=\s*"([^"]+)"', (ROOT / "pyproject.toml").read_text(), re.MULTILINE).group(1)
    npm = json.loads((ROOT / "npm/package.json").read_text())["version"]
    server = json.loads((ROOT / "server.json").read_text())["version"]
    assert {py_version, npm, server} == {project}
    for package in json.loads((ROOT / "server.json").read_text())["packages"]:
        assert package["version"] == project


def test_npm_version_command_reports_package_without_installing_engine():
    node = shutil.which("node")
    if not node:
        pytest.skip("Node is optional for Python-only installations")
    result = subprocess.run([node, str(ROOT / "npm/cli.js"), "--version"], capture_output=True, text=True, timeout=5)
    package = json.loads((ROOT / "npm/package.json").read_text())
    assert result.returncode == 0
    assert result.stdout.strip() == f"imprint {package['version']}"
    assert result.stderr == ""
