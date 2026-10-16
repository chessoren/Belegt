#!/bin/sh
# Record the demo live inside the offline namespace, plus proof output and offline screenshots.
#   sudo scripts/video/record_offline.sh OUT_DIR
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
OUT=${1:-$ROOT/../video-frames}
mkdir -p "$OUT"
exec unshare -n sh -c "
  python3 '$ROOT/scripts/lo_up.py' >/dev/null
  {
    unset HTTPS_PROXY HTTP_PROXY https_proxy http_proxy ALL_PROXY all_proxy
    echo '\$ cat /proc/net/route'; cat /proc/net/route
    echo '\$ curl -m 5 https://www.fedlex.admin.ch'; curl -sS -m 5 https://www.fedlex.admin.ch -o /dev/null 2>&1 || true
    echo '\$ python3 -c \"import socket; socket.create_connection((\\\"1.1.1.1\\\", 443), 3)\"'
    python3 -c 'import socket; socket.create_connection((\"1.1.1.1\", 443), 3)' 2>&1 | tail -1
  } > '$OUT/proof.txt' 2>&1
  '$ROOT/scripts/start.sh' > '$OUT/server.log' 2>&1 &
  until curl -sf http://127.0.0.1:8080/api/status >/dev/null 2>&1; do sleep 1; done
  curl -s http://127.0.0.1:8080/api/status > '$OUT/status.json'
  node '$ROOT/scripts/video/record.mjs' '$OUT'
  node '$ROOT/scripts/video/offline_shots.mjs' '$ROOT/docs/img'
  curl -s http://127.0.0.1:8080/api/status > '$OUT/status_after.json'
"
