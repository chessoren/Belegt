"""Fill every document with the real numbers from eval/summary.json.

    python scripts/fill_numbers.py
Templates: docs/*.template.md -> docs/*.md ; README results block ; video line l10.
"""
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
S = json.loads((ROOT / "eval" / "summary.json").read_text())
M = S["metrics"]


def pct(k, who):
    v = M[k]
    return round(100 * v[who] / v["n"]) if v["n"] else 0


def f(k, who):
    v = M[k]
    return v[f"{who}_fmt"]


video = ROOT / "docs" / "video" / "Belegt-demo.mp4"
vlen = "≈ 2 min"
if video.exists():
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
                             capture_output=True, text=True).stdout or 0)
    vlen = f"{int(d // 60)}:{int(d % 60):02d}"

V = {
    "RUN": "eval/runs/run.jsonl", "N": S["n_items"], "N_ANS": S["answerable"], "N_TRAP": S["traps"],
    "WRONG_BASE": pct("wrong_article_published", "baseline"), "WRONG_BELEGT": pct("wrong_article_published", "belegt"),
    "CORRECT_BASE_F": f("correct_article", "baseline"), "CORRECT_BELEGT_F": f("correct_article", "belegt"),
    "WRONG_BASE_F": f("wrong_article_published", "baseline"), "WRONG_BELEGT_F": f("wrong_article_published", "belegt"),
    "TRAP_BASE_F": f("trap_refused", "baseline"), "TRAP_BELEGT_F": f("trap_refused", "belegt"),
    "LANG_BASE_F": f("lang_agree", "baseline"), "LANG_BELEGT_F": f("lang_agree", "belegt"),
    "OVER_BELEGT_F": f("over_refusal", "belegt"),
    "TRAP_BASE": pct("trap_refused", "baseline"), "TRAP_BELEGT": pct("trap_refused", "belegt"),
    "LANG_BASE": pct("lang_agree", "baseline"), "LANG_BELEGT": pct("lang_agree", "belegt"),
    "CORRECT_BASE": pct("correct_article", "baseline"), "CORRECT_BELEGT": pct("correct_article", "belegt"),
    "OVER_BELEGT": pct("over_refusal", "belegt"),
    "TRAP_N": M["trap_refused"]["n"], "TRAP_K": M["trap_refused"]["belegt"],
    "V_REJ": S["verifier"]["quotes_rejected"], "V_REM": S["verifier"]["sentences_removed"],
    "LAT": S["latency_seconds"]["median"], "VIDEO_LEN": vlen,
}


def fill(text):
    def rep(m):
        k = m.group(1)
        if k not in V:
            raise KeyError(k)
        return str(V[k])
    return re.sub(r"\{\{([A-Z_]+)\}\}", rep, text)


for t in (ROOT / "docs").glob("*.template.md"):
    out = t.with_name(t.name.replace(".template", ""))
    out.write_text(fill(t.read_text()))
    print("wrote", out.relative_to(ROOT))

# README block
readme = ROOT / "README.md"
r = readme.read_text()
block = fill("""<!-- RESULTS:START -->
| {{N}} questions ({{N_ANS}} answerable, {{N_TRAP}} traps) | Apertus alone | Apertus + Belegt |
|---|---|---|
| Cites a correct article | {{CORRECT_BASE_F}} | **{{CORRECT_BELEGT_F}}** |
| Publishes a wrong or invented article | {{WRONG_BASE_F}} | **{{WRONG_BELEGT_F}}** |
| Trap questions refused | {{TRAP_BASE_F}} | **{{TRAP_BELEGT_F}}** |
| Same answer in all 4 languages | {{LANG_BASE_F}} | **{{LANG_BELEGT_F}}** |
| Abstains although an answer exists | — | {{OVER_BELEGT_F}} |

Median latency {{LAT}} s per answer on 4 CPU cores. 95% Wilson intervals.
<!-- RESULTS:END -->""")
r = re.sub(r"<!-- RESULTS:START -->.*<!-- RESULTS:END -->", lambda m: block, r, flags=re.S)
readme.write_text(r)

# video numbers line
sp = ROOT / "docs" / "video" / "script.json"
s = json.loads(sp.read_text())
for line in s["lines"]:
    if line["id"] == "l10":
        line["fr"] = fill("Même modèle, mêmes questions. Seul, Apertus cite un article faux ou inventé dans {{WRONG_BASE}} pour cent des cas. Avec Bélèkt, {{WRONG_BELEGT}} pour cent. Et il refuse {{TRAP_K}} pièges sur {{TRAP_N}}. Mesuré, ouvert, réutilisable.")
        line["sub_fr"] = fill("Même modèle, mêmes questions. Article faux ou inventé : {{WRONG_BASE}} % seul, {{WRONG_BELEGT}} % avec Belegt. Pièges refusés : {{TRAP_K}}/{{TRAP_N}}.")
        line["sub_en"] = fill("Same model, same questions. Wrong or invented article: {{WRONG_BASE}}% alone, {{WRONG_BELEGT}}% with Belegt. Traps refused: {{TRAP_K}}/{{TRAP_N}}.")
sp.write_text(json.dumps(s, ensure_ascii=False, indent=1))
print(json.dumps({k: V[k] for k in ("WRONG_BASE", "WRONG_BELEGT", "TRAP_K", "TRAP_N", "LANG_BASE", "LANG_BELEGT")}))
