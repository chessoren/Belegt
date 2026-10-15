#!/bin/sh
# Start Apertus (llama.cpp) and Belegt on this machine.
#   LLAMA_SERVER=/path/to/llama-server MODEL=/path/to/apertus.gguf scripts/start.sh
set -e
ROOT=$(cd "$(dirname "$0")/.." && pwd)
LLAMA_SERVER=${LLAMA_SERVER:-$ROOT/../models/llama.cpp/build/bin/llama-server}
MODEL=${MODEL:-$ROOT/../models/apertus-v1.5-8b-text-q4_k_m.gguf}
THREADS=${THREADS:-$(nproc)}
PORT=${PORT:-8080}
if ! curl -sf http://127.0.0.1:8081/health >/dev/null 2>&1; then
  "$LLAMA_SERVER" -m "$MODEL" --host 127.0.0.1 --port 8081 -c 8192 -t "$THREADS" --jinja --no-webui >"${TMPDIR:-/tmp}/belegt-llama.log" 2>&1 &
  echo "waiting for Apertus…"
  until curl -sf http://127.0.0.1:8081/health >/dev/null 2>&1; do sleep 1; done
fi
export BELEGT_MODEL_PATH="$MODEL"
cd "$ROOT" && exec python3 -m belegt.server --port "$PORT"
