#!/bin/sh
# Run the whole stack inside a fresh Linux network namespace that has NO
# network interface except loopback: the strongest "cable unplugged" test.
#   sudo scripts/offline_demo.sh            # then run a browser in the same namespace,
#   sudo scripts/offline_demo.sh CMD...     # or pass a command to run next to the server.
ROOT=$(cd "$(dirname "$0")/.." && pwd)
exec unshare -n sh -c "
  python3 '$ROOT/scripts/lo_up.py' >/dev/null
  echo '--- network check inside the namespace ---'
  cat /proc/net/route
  (curl -s -m 3 https://www.fedlex.admin.ch >/dev/null && echo 'fedlex reachable?!') || echo 'fedlex.admin.ch: unreachable (expected)'
  '$ROOT/scripts/start.sh' &
  until curl -sf http://127.0.0.1:${PORT:-8080}/api/status >/dev/null 2>&1; do sleep 1; done
  echo 'Belegt is up, offline, on http://127.0.0.1:${PORT:-8080}'
  if [ \$# -gt 0 ]; then \"\$@\"; else wait; fi
" sh "$@"
