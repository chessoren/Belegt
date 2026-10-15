"""Run the evaluation: Apertus alone vs. Apertus + Belegt, same local model.

    python eval/run_eval.py --out eval/runs/run.jsonl

Resumable: items already present in the output file are skipped.
Raw outputs are kept so that every number in the report can be audited.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from belegt import llm  # noqa: E402
from belegt.pipeline import Belegt  # noqa: E402

BASELINE_INSTR = {
    "fr": "Réponds en 2 à 3 phrases et indique le numéro de l'article de la Constitution fédérale suisse.",
    "de": "Antworte in 2 bis 3 Sätzen und nenne die Artikelnummer der schweizerischen Bundesverfassung.",
    "it": "Rispondi in 2-3 frasi e indica il numero dell'articolo della Costituzione federale svizzera.",
    "rm": "Respunda en 2 fin 3 frasas e numna il numer da l'artitgel da la Constituziun federala svizra.",
}


def baseline(q: str, lang: str) -> dict:
    r = llm.chat([{"role": "user", "content": q + "\n" + BASELINE_INSTR[lang]}], max_tokens=220)
    return {"text": r["text"], "seconds": r["seconds"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--questions", default=str(ROOT / "eval" / "questions.jsonl"))
    ap.add_argument("--out", default=str(ROOT / "eval" / "runs" / "run.jsonl"))
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if out.exists():
        done = {json.loads(l)["id"] for l in out.read_text().splitlines() if l.strip()}
    items = [json.loads(l) for l in Path(a.questions).read_text().splitlines() if l.strip()]
    if a.only:
        items = [i for i in items if i["id"] in a.only.split(",")]
    engine = Belegt()
    for it in items:
        if it["id"] in done:
            continue
        t0 = time.time()
        res = None
        for ev in engine.run(it["q"], it["lang"]):
            if ev["type"] == "result":
                res = ev
        base = baseline(it["q"], it["lang"])
        row = {
            **it,
            "belegt": {k: res[k] for k in ("decision", "answer", "model_said_answerable", "model_answer_raw",
                                         "model_citations_raw", "citations", "rejected", "removed_sentences",
                                         "sentences", "consistency", "consistency_ok", "per_lang_articles",
                                         "nearest", "seconds", "timings")},
            "baseline": base,
            "wall_seconds": round(time.time() - t0, 1),
        }
        row["belegt"]["receipt_id"] = res["receipt"]["receipt_id"]
        with out.open("a") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"{it['id']:8} {res['decision']:10} cites={[c['label'] for c in res['citations']]} "
              f"base={base['text'][:70]!r} {row['wall_seconds']}s", flush=True)


if __name__ == "__main__":
    main()
