#!/usr/bin/env python3
"""Imprint live-demo render service.

Public demo endpoint: POST /render  {"markdown": "...", "theme": "auto|name"}
Returns the generated PDF with X-Imprint-* headers (score/pages/theme).
Rate-limited per IP, size-capped, rendered in a timed-out subprocess.
"""
import json
import os
import re
import subprocess
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = os.environ.get("IMPRINT_DEMO_HOST", "127.0.0.1")
PORT = int(os.environ.get("IMPRINT_DEMO_PORT", "8899"))
PYTHON = os.environ.get("IMPRINT_DEMO_PYTHON", "python3")
MAX_BODY = 300 * 1024
MAX_PAGES = 40
RENDER_TIMEOUT = 120
RATE_LIMIT = int(os.environ.get("IMPRINT_DEMO_RATE", "20"))  # per hour per IP

_theme_cache = {"names": None, "at": 0.0}
_lock = threading.Lock()
_hits: dict[str, list[float]] = {}


def list_themes() -> list[str]:
    now = time.time()
    with _lock:
        if _theme_cache["names"] is None or now - _theme_cache["at"] > 300:
            try:
                out = subprocess.run(
                    [PYTHON, "-m", "imprint", "--list-themes"],
                    capture_output=True, text=True, timeout=30,
                )
                names = [n.strip() for n in out.stdout.splitlines() if n.strip()]
                _theme_cache["names"] = names
                _theme_cache["at"] = now
            except Exception:
                return _theme_cache["names"] or []
    return _theme_cache["names"] or []


def rate_ok(ip: str) -> bool:
    now = time.time()
    with _lock:
        times = [t for t in _hits.get(ip, []) if now - t < 3600]
        if len(times) >= RATE_LIMIT:
            _hits[ip] = times
            return False
        times.append(now)
        _hits[ip] = times
    return True


def render(markdown: str, theme: str) -> tuple[bytes, dict]:
    with tempfile.TemporaryDirectory(prefix="imprint-demo-") as td:
        src = os.path.join(td, "input.md")
        out = os.path.join(td, "output.pdf")
        rpt = os.path.join(td, "report.json")
        with open(src, "w", encoding="utf-8") as f:
            f.write(markdown)
        cmd = [PYTHON, "-m", "imprint", src, "--out", out, "--report", rpt]
        if theme and theme != "auto":
            cmd += ["--theme", theme]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=RENDER_TIMEOUT)
        if not os.path.exists(out):
            err = (proc.stderr or proc.stdout or "unknown error")[-800:]
            raise RuntimeError(f"render failed: {err}")
        pdf = open(out, "rb").read()
        info = {"pages": 0, "score": 0.0, "theme": theme or "auto"}
        if os.path.exists(rpt):
            try:
                rep = json.load(open(rpt, encoding="utf-8"))
                info["score"] = rep.get("score", 0)
                info["pages"] = rep.get("pages", 0)
                info["theme"] = rep.get("theme") or info["theme"]
            except Exception:
                pass
        if info["pages"] > MAX_PAGES:
            raise RuntimeError(f"too many pages ({info['pages']} > {MAX_PAGES})")
        return pdf, info


class Handler(BaseHTTPRequestHandler):
    server_version = "ImprintDemo/1.0"

    def log_message(self, fmt, *args):
        pass

    def _send(self, code, body=b"", ctype="text/plain; charset=utf-8", headers=None):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Expose-Headers", "X-Imprint-Score, X-Imprint-Pages, X-Imprint-Theme, Content-Disposition")
        for k, v in (headers or {}).items():
            self.send_header(k, str(v))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path in ("/", "/healthz"):
            self._send(200, b"imprint demo ok\n")
        elif self.path.startswith("/themes"):
            payload = json.dumps({"themes": list_themes()}).encode()
            self._send(200, payload, "application/json")
        else:
            self._send(404, b"not found")

    def do_POST(self):
        ip = self.client_address[0]
        if not rate_ok(ip):
            self._send(429, b"rate limited: too many requests")
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
        except ValueError:
            length = 0
        if length <= 0 or length > MAX_BODY:
            self._send(413, b"body too large (max 300KB)")
            return
        try:
            data = json.loads(self.rfile.read(length))
        except Exception:
            self._send(400, b"invalid JSON")
            return
        markdown = (data.get("markdown") or "").strip()
        theme = (data.get("theme") or "auto").strip().lower()
        if not markdown:
            self._send(400, b"missing markdown")
            return
        themes = list_themes()
        if theme != "auto" and theme not in themes:
            self._send(400, json.dumps({"error": f"unknown theme; available: {themes[:12]} ..."}).encode())
            return
        try:
            pdf, info = render(markdown, theme)
        except subprocess.TimeoutExpired:
            self._send(504, b"render timeout")
            return
        except RuntimeError as e:
            self._send(422, str(e).encode()[:400])
            return
        headers = {
            "X-Imprint-Score": f"{info['score']:.1f}",
            "X-Imprint-Pages": str(info["pages"]),
            "X-Imprint-Theme": info["theme"],
            "Content-Disposition": "inline; filename=imprint.pdf",
        }
        self._send(200, pdf, "application/pdf", headers)


if __name__ == "__main__":
    print(f"imprint demo on http://{HOST}:{PORT} (python={PYTHON}) themes={len(list_themes())}")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
