"""Build the static public demo (Netlify) into site/: the real UI replaying real recorded runs.
    python scripts/build_static.py"""
import json, shutil
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site"
shutil.rmtree(OUT, ignore_errors=True)
shutil.copytree(ROOT / "web", OUT)
html = (OUT / "index.html").read_text().replace('<script src="/i18n.js"></script>', '<script>window.BELEGT_STATIC = true;</script>\n<script src="/i18n.js"></script>')
(OUT / "index.html").write_text(html)
langs = ("de", "fr", "it", "rm")
corpus = {l: json.loads((ROOT / "data" / "corpus" / f"{l}.json").read_text()) for l in langs}
man = json.loads((ROOT / "data" / "corpus" / "manifest.json").read_text())
arts = sorted({r["article"] for r in corpus["de"]})
(OUT / "data" / "articles").mkdir(parents=True, exist_ok=True)
for a in arts:
    (OUT / "data" / "articles" / f"{a}.json").write_text(json.dumps({"id": a, "languages": {l: [r for r in corpus[l] if r["article"] == a] for l in langs}, "urls": {l: man["languages"][l]["url"] for l in langs}}, ensure_ascii=False))
idx = []
for p in sorted((OUT / "data" / "replays").glob("*.json")):
    if p.name == "index.json":
        continue
    ev = json.loads(p.read_text())
    res = ev[-1]
    if res.get("type") != "result":
        continue
    idx.append({"name": p.stem, "q": res["receipt"]["question"], "lang": res["lang"], "decision": res["decision"]})
(OUT / "data" / "replays" / "index.json").write_text(json.dumps(idx, ensure_ascii=False, indent=1))
# status snapshot (taken inside the offline namespace during the recording)
snap = Path("/home/user/video-frames-en/status_after.json")
st = json.loads(snap.read_text()) if snap.exists() else {"network": {"offline": True, "outbound_attempts": 0}}
(OUT / "data" / "status.json").write_text(json.dumps(st))
(OUT / "_redirects").write_text("/api/*  /index.html  404\n")
print(len(arts), "articles;", len(idx), "replays:", [i["name"] for i in idx])
