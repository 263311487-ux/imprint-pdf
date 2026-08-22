#!/usr/bin/env bash
# 发布 imprint-pdf 到 PyPI (需先跑 pypi_finish.py 拿到 token)
set -euo pipefail
cd "$(dirname "$0")"
CRED="$HOME/Desktop/账号凭证/pypi_credential.txt"
if [ ! -f "$CRED" ]; then echo "先跑 pypi_finish.py"; exit 1; fi
TOKEN=$(grep -o "PYPI_TOKEN=.*" "$CRED" | cut -d= -f2)
VERSION=$(grep "^version" pyproject.toml | cut -d= -f2 | tr -d " \"")
[ -f "dist/imprint_pdf-${VERSION}-py3-none-any.whl" ] || .venv/bin/python -m build --outdir dist
UV_PUBLISH_TOKEN="$TOKEN" uv publish --publish-url https://upload.pypi.org/legacy/ "dist/imprint_pdf-${VERSION}-"*.whl "dist/imprint_pdf-${VERSION}.tar.gz"
echo "发布完成: https://pypi.org/project/imprint-pdf/${VERSION}/"
