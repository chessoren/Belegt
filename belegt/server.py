"""Belegt HTTP server. Python standard library only.

    python -m belegt.server --port 8080

Serves the web UI from ./web and a small JSON/SSE API:
    GET  /api/status                 model, corpus, network, outbound counter
    POST /api/ask                    {"question": "...", "lang": "fr"} -> text/event-stream
    GET  /api/article?id=art_22      the article in DE/FR/IT/RM
Nothing is stored server-side: questions and receipts live in the browser.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import os
import threading
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from . import llm, netguard
from .corpus import LANGS, ROOT
from .pipeline import Belegt

WEB = ROOT / "web"
MODEL_PATH = Path(os.environ.get("BELEGT_MODEL_PATH", str(ROOT.parent / "models" / llm.MODEL_FILE)))
_model_sha = {"value": None}
_ask_lock = threading.Lock()  # one CPU, one question at a time


def _hash_model():
    cache = ROOT / "data" / "model.sha256.json"
    try:
        st = MODEL_PATH.stat()
    except OSError:
        _model_sha["value"] = "model file not found"
        return
    key = f"{MODEL_PATH.name}:{st.st_size}:{int(st.st_mtime)}"
    if cache.exists():
        c = json.loads(cache.read_text())
        if c.get("key") == key:
            _model_sha["value"] = c["sha256"]
            return
    h = hashlib.sha256()
    with open(MODEL_PATH, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    _model_sha["value"] = h.hexdigest()
    cache.write_text(json.dumps({"key": key, "file": MODEL_PATH.name, "sha256": _model_sha["value"]}, indent=2))


ENGINE: Belegt | None = None


class Handler(BaseHTTPRequestHandler):
    server_version = "Belegt/1.0"

    def log_message(self, fmt, *args):  # quiet
        pass

    def _json(self, obj, code=200):
        data = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/api/status":
            m = ENGINE.corpus.manifest
            return self._json({
                "model": {**llm.health(), "file": llm.MODEL_FILE, "sha256": _model_sha["value"]},
                "corpus": {"sr": m["sr"], "version": m["version"], "eli": m["eli"],
                           "languages": {l: m["languages"][l]["paragraphs"] for l in LANGS},
                           "fingerprint": ENGINE.corpus.fingerprint()},
                "network": netguard.state(),
            })
        if u.path == "/api/article":
            q = parse_qs(u.query)
            art = (q.get("id") or [""])[0]
            out = {l: ENGINE.corpus.article_paragraphs(l, art) for l in LANGS}
            if not out["de"]:
                return self._json({"error": "unknown article"}, 404)
            return self._json({"id": art, "languages": out, "urls": {l: ENGINE.corpus.manifest["languages"][l]["url"] for l in LANGS}})
        return self._static(u.path)

    def do_POST(self):
        u = urlparse(self.path)
        if u.path != "/api/ask":
            return self._json({"error": "not found"}, 404)
        n = int(self.headers.get("Content-Length") or 0)
        try:
            body = json.loads(self.rfile.read(n) or b"{}")
        except json.JSONDecodeError:
            return self._json({"error": "bad json"}, 400)
        question = (body.get("question") or "").strip()[:500]
        if not question:
            return self._json({"error": "empty question"}, 400)
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Accel-Buffering", "no")
        self.end_headers()

        def send(ev):
            self.wfile.write(("data: " + json.dumps(ev, ensure_ascii=False) + "\n\n").encode())
            self.wfile.flush()

        if not _ask_lock.acquire(blocking=False):
            send({"type": "step", "step": "queue", "status": "start"})
            _ask_lock.acquire()
        try:
            for ev in ENGINE.run(question, body.get("lang")):
                send(ev)
        except BrokenPipeError:
            pass
        except Exception as e:  # noqa: BLE001
            traceback.print_exc()
            try:
                send({"type": "error", "message": str(e)})
            except BrokenPipeError:
                pass
        finally:
            _ask_lock.release()

    def _static(self, path: str):
        if path in ("", "/"):
            path = "/index.html"
        p = (WEB / path.lstrip("/")).resolve()
        if not str(p).startswith(str(WEB.resolve())) or not p.is_file():
            p = WEB / "index.html"
        data = p.read_bytes()
        ctype = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
        if p.suffix == ".woff2":
            ctype = "font/woff2"
        self.send_response(200)
        self.send_header("Content-Type", ctype + ("; charset=utf-8" if ctype.startswith("text/") or ctype.endswith("javascript") else ""))
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(data)


def main():
    global ENGINE
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8080)
    a = ap.parse_args()
    netguard.install()
    threading.Thread(target=_hash_model, daemon=True).start()
    ENGINE = Belegt(model_sha256=lambda: _model_sha["value"], network_state=netguard.state)
    srv = ThreadingHTTPServer((a.host, a.port), Handler)
    print(f"Belegt listening on http://{a.host}:{a.port}  (model: {llm.LLM_URL})")
    srv.serve_forever()


if __name__ == "__main__":
    main()
