"""Record the real event stream of one question, for docs and screenshots.
    python scripts/record_replay.py manifester "Ai-je le droit de manifester dans la rue ?"
"""
import json, sys, urllib.request
from pathlib import Path
name, q = sys.argv[1], sys.argv[2]
port = sys.argv[3] if len(sys.argv) > 3 else "8080"
req = urllib.request.Request(f"http://127.0.0.1:{port}/api/ask", data=json.dumps({"question": q}).encode(),
                             headers={"Content-Type": "application/json"})
events = []
with urllib.request.urlopen(req, timeout=900) as r:
    for raw in r:
        line = raw.decode().strip()
        if line.startswith("data:"):
            events.append(json.loads(line[5:]))
out = Path(__file__).resolve().parent.parent / "web" / "data" / "replays" / f"{name}.json"
out.write_text(json.dumps(events, ensure_ascii=False))
res = events[-1]
print(name, res.get("decision"), res.get("seconds"), [c["label"] for c in res.get("citations", [])])
