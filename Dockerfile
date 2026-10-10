# Source checkout image; this does not replace the published PyPI artifact.
FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0 \
        fontconfig fonts-noto-cjk fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/imprint
COPY pyproject.toml README.md LICENSE ./
COPY imprint/ ./imprint/
RUN python -m pip install --no-cache-dir '.[mcp]' 'mcp==1.30.0' \
    && useradd --create-home --uid 10001 imprint \
    && mkdir /work \
    && chown imprint:imprint /work

USER imprint
WORKDIR /work
ENTRYPOINT ["imprint-mcp"]
