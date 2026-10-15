"""Client for a *local* llama.cpp server running Apertus.

Only loopback addresses are accepted: Belegt refuses to send a citizen's
question to any remote host. The model weights live on the machine.
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from urllib.parse import urlparse

LLM_URL = os.environ.get("BELEGT_LLM_URL", "http://127.0.0.1:8081")
MODEL_FILE = os.environ.get("BELEGT_MODEL_FILE", "apertus-v1.5-8b-text-q4_k_m.gguf")
MODEL_NAME = os.environ.get("BELEGT_MODEL_NAME", "Apertus 1.5 8B (swiss-ai, Q4_K_M GGUF)")

_host = urlparse(LLM_URL).hostname
if _host not in ("127.0.0.1", "localhost", "::1"):
    raise SystemExit(f"Belegt only talks to a local model; refusing BELEGT_LLM_URL={LLM_URL}")


def chat(messages: list[dict], *, schema: dict | None = None, max_tokens: int = 400,
         temperature: float = 0.0, seed: int = 42, timeout: int = 600, on_token=None) -> dict:
    """Call the local OpenAI-compatible endpoint. Returns text + timings.
    If ``schema`` is given, decoding is constrained to that JSON schema
    (llama.cpp grammar), so the output is always parseable."""
    body = {
        "messages": messages,
        "temperature": temperature,
        "seed": seed,
        "max_tokens": max_tokens,
        "cache_prompt": True,
        "stream": on_token is not None,
    }
    if schema is not None:
        body["response_format"] = {"type": "json_schema", "json_schema": {"name": "out", "schema": schema}}
    req = urllib.request.Request(
        LLM_URL + "/v1/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
    )
    t0 = time.time()
    for attempt in range(6):  # the local server answers 503 while loading or saturated
        try:
            r = urllib.request.urlopen(req, timeout=timeout)
            break
        except urllib.error.HTTPError as e:
            if e.code != 503 or attempt == 5:
                raise
            time.sleep(2 + 3 * attempt)
    with r:
        if on_token is None:
            d = json.loads(r.read())
            text = d["choices"][0]["message"].get("content") or ""
            timings = d.get("timings", {})
        else:
            text, timings = "", {}
            for raw in r:
                line = raw.decode("utf-8", "ignore").strip()
                if not line.startswith("data:"):
                    continue
                payload = line[5:].strip()
                if payload == "[DONE]":
                    break
                d = json.loads(payload)
                if d.get("timings"):
                    timings = d["timings"]
                for ch in d.get("choices", []):
                    piece = (ch.get("delta") or {}).get("content") or ""
                    if piece:
                        text += piece
                        on_token(piece)
    return {"text": text, "seconds": round(time.time() - t0, 2), "timings": timings}


def health() -> dict:
    try:
        with urllib.request.urlopen(LLM_URL + "/health", timeout=2) as r:
            ok = r.status == 200
        return {"ok": ok, "url": LLM_URL, "model": MODEL_NAME}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "url": LLM_URL, "model": MODEL_NAME, "error": str(e)}
