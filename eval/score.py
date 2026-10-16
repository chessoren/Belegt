"""Score an evaluation run and write the report.

    python eval/score.py eval/runs/run.jsonl

Writes eval/results.md, eval/summary.json and web/data/eval-summary.json.
Trap answers of the baseline are labelled by hand (eval/manual_labels.json),
because "does this free-text answer invent an article?" is not something we
want to decide with a regex. Every label carries a one-line justification.
"""
from __future__ import annotations

import json
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from belegt.verify import art_numbers  # noqa: E402


def wilson(k: int, n: int, z: float = 1.96):
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (p, max(0.0, c - h), min(1.0, c + h))


def fmt(k, n):
    p, lo, hi = wilson(k, n)
    return f"{k}/{n} = {100 * p:.0f}% [{100 * lo:.0f}–{100 * hi:.0f}]"


def num(a: str) -> str:
    return a.replace("art_", "").replace("_", "").lower()


def main(path: str):
    rows = [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]
    labels_path = ROOT / "eval" / "manual_labels.json"
    labels = json.loads(labels_path.read_text()) if labels_path.exists() else {}

    per = []
    for r in rows:
        gold = {num(a) for a in r["gold"]}
        b = r["belegt"]
        b_arts = {c["art_num"].lower() for c in b["citations"]}
        base_arts = art_numbers(r["baseline"]["text"])
        raw_arts = art_numbers(b["model_answer_raw"]) if b["model_said_answerable"] else set()
        trap = not r["gold"]
        rec = {
            "id": r["id"], "lang": r["lang"], "set": r["set"], "of": r.get("of", r["id"]), "trap": trap,
            "b_decision": b["decision"], "b_arts": sorted(b_arts),
            "b_correct": (not trap) and bool(b_arts & gold),
            "b_wrong": bool(b_arts - gold) if not trap else (b["decision"] == "answered"),
            "b_abstain": b["decision"] == "abstained",
            "base_arts": sorted(base_arts),
            "base_correct": (not trap) and bool(base_arts & gold),
            "base_wrong": bool(base_arts - gold),
            "rejected": len(b["rejected"]), "removed": len(b["removed_sentences"]),
            "raw_wrong": bool(raw_arts - gold) if not trap else b["model_said_answerable"],
            "model_said_answerable": b["model_said_answerable"],
            "seconds": b["seconds"],
        }
        if trap:
            lab = labels.get(r["id"], {})
            # baseline trap outcome: "invented" (asserts an article answers it), "refused", "unclear"
            rec["base_trap"] = lab.get("baseline", "unlabelled")
            rec["base_wrong"] = rec["base_trap"] == "invented"
        per.append(rec)

    ans = [p for p in per if not p["trap"]]
    traps = [p for p in per if p["trap"]]
    out = {}
    out["n_items"] = len(per)
    out["answerable"] = len(ans)
    out["traps"] = len(traps)
    m = {}
    m["correct_article"] = (sum(p["base_correct"] for p in ans), sum(p["b_correct"] for p in ans), len(ans))
    m["wrong_article_published"] = (sum(p["base_wrong"] for p in per), sum(p["b_wrong"] for p in per), len(per))
    m["wrong_on_answerable"] = (sum(p["base_wrong"] for p in ans), sum(p["b_wrong"] for p in ans), len(ans))
    m["over_refusal"] = (0, sum(p["b_abstain"] for p in ans), len(ans))
    m["trap_refused"] = (sum(p.get("base_trap") == "refused" for p in traps), sum(p["b_abstain"] for p in traps), len(traps))
    m["trap_invented"] = (sum(p.get("base_trap") == "invented" for p in traps), sum(not p["b_abstain"] for p in traps), len(traps))
    for lg in ("fr", "de", "it", "rm"):
        sub = [p for p in ans if p["lang"] == lg]
        if sub:
            m[f"correct_{lg}"] = (sum(p["base_correct"] for p in sub), sum(p["b_correct"] for p in sub), len(sub))

    # cross-language agreement on the parallel groups (same question in DE/FR/IT/RM)
    groups = defaultdict(list)
    for p in per:
        if p["set"] == "parallel" or any(q["of"] == p["id"] for q in per if q["set"] == "parallel"):
            groups[p["of"]].append(p)
    groups = {k: v for k, v in groups.items() if len(v) == 4}
    b_agree = sum(1 for v in groups.values() if len({(x["b_decision"], tuple(x["b_arts"])) for x in v}) == 1)
    base_agree = sum(1 for v in groups.values() if len({tuple(x["base_arts"]) for x in v}) == 1)
    m["lang_agree"] = (base_agree, b_agree, len(groups))

    # verifier activity (what the deterministic layer caught)
    out["verifier"] = {
        "quotes_rejected": sum(p["rejected"] for p in per),
        "answers_with_rejected_quote": sum(1 for p in per if p["rejected"]),
        "sentences_removed": sum(p["removed"] for p in per),
        "rag_without_verifier_wrong": sum(p["raw_wrong"] for p in per),
        "model_said_answerable_but_abstained": sum(1 for p in per if p["model_said_answerable"] and p["b_abstain"]),
    }
    secs = [p["seconds"] for p in per]
    out["latency_seconds"] = {"median": round(statistics.median(secs), 1), "p90": round(sorted(secs)[int(.9 * len(secs)) - 1], 1)}
    out["metrics"] = {k: {"baseline": v[0], "belegt": v[1], "n": v[2],
                          "baseline_fmt": fmt(v[0], v[2]), "belegt_fmt": fmt(v[1], v[2])} for k, v in m.items()}
    out["items"] = per
    (ROOT / "eval" / "summary.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))

    # ---- markdown report
    L = []
    L.append("# Belegt — evaluation results\n")
    L.append(f"Run file: `{Path(path).relative_to(ROOT)}` · {len(per)} items ({len(ans)} answerable, {len(traps)} traps) · "
             f"model: Apertus 1.5 8B Q4_K_M, local llama.cpp on 4 CPU cores, temperature 0.\n")
    L.append("Both systems use **the same local model**. *Baseline* = Apertus asked directly (asked to name the article). "
             "*Belegt* = Apertus + retrieval + deterministic verifier. 95% Wilson intervals in brackets.\n")
    L.append("| Metric | Apertus alone | Apertus + Belegt |\n|---|---|---|")
    names = {
        "correct_article": "Cites a correct article (answerable questions)",
        "wrong_article_published": "Publishes a wrong or invented article (all items)",
        "wrong_on_answerable": "Publishes a wrong article (answerable questions)",
        "over_refusal": "Abstains although an answer exists",
        "trap_refused": "Trap questions refused",
        "trap_invented": "Trap questions answered with an article",
        "correct_fr": "Correct article — French", "correct_de": "Correct article — German",
        "correct_it": "Correct article — Italian", "correct_rm": "Correct article — Romansh",
        "lang_agree": "Same answer in all 4 languages (parallel groups)",
    }
    for k, v in out["metrics"].items():
        base = v["baseline_fmt"] if k != "over_refusal" else "n/a (never abstains)"
        L.append(f"| {names.get(k, k)} | {base} | **{v['belegt_fmt']}** |")
    vv = out["verifier"]
    L.append("\n## What the verifier caught\n")
    L.append(f"- Quotes rejected because they were not found word for word: **{vv['quotes_rejected']}** "
             f"(in {vv['answers_with_rejected_quote']} answers).")
    L.append(f"- Sentences removed because they named an unproven article: **{vv['sentences_removed']}**.")
    L.append(f"- Answers where the model said 'answerable' but no evidence survived (Belegt abstained): "
             f"**{vv['model_said_answerable_but_abstained']}**.")
    L.append(f"- Ablation, retrieval *without* verifier: raw drafts that name a wrong article: **{vv['rag_without_verifier_wrong']}**.")
    ho = [p for p in per if p["id"].startswith("h")]
    if ho:
        ha = [p for p in ho if not p["trap"]]; ht = [p for p in ho if p["trap"]]
        L.append("\n## Held-out questions (written after the last design change)\n")
        L.append(f"- Answerable: correct article Apertus alone {fmt(sum(p['base_correct'] for p in ha), len(ha))} · Belegt {fmt(sum(p['b_correct'] for p in ha), len(ha))}")
        L.append(f"- Traps refused: Apertus alone {fmt(sum(p.get('base_trap') == 'refused' for p in ht), len(ht))} · Belegt {fmt(sum(p['b_abstain'] for p in ht), len(ht))}")
    L.append("\n## Weakness map (every Belegt failure, kept visible)\n")
    for p, r in zip(per, rows):
        if p["trap"] and not p["b_abstain"]:
            L.append(f"- **{p['id']}** ({p['lang']}) trap answered: {r['q']}")
        elif not p["trap"] and p["b_abstain"]:
            L.append(f"- **{p['id']}** ({p['lang']}) wrongful abstention — gold {', '.join(r['gold'])}; closest shown: {', '.join(n['label'] for n in r['belegt']['nearest'])} — {r['q']}")
        elif not p["trap"] and p["b_wrong"]:
            L.append(f"- **{p['id']}** ({p['lang']}) real quote, wrong article — cited {', '.join(p['b_arts'])}, gold {', '.join(r['gold'])} — {r['q']}")
    L.append("\nScoring is conservative: a real quote from a neighbouring article counts as an error even when it is "
             "defensible (e.g. Art. 70 *official languages* cited next to Art. 4, or the transitional provision of Art. 196 "
             "on the direct federal tax).")
    L.append(f"\nLatency per answer (CPU, 4 cores): median {out['latency_seconds']['median']} s, p90 {out['latency_seconds']['p90']} s.\n")
    L.append("## Every item\n")
    L.append("| id | lang | gold | Belegt | Belegt articles | baseline articles | baseline trap label |\n|---|---|---|---|---|---|---|")
    for p, r in zip(per, rows):
        L.append(f"| {p['id']} | {p['lang']} | {', '.join(num(a) for a in r['gold']) or '—'} | {p['b_decision']} | "
                 f"{', '.join(p['b_arts']) or '—'} | {', '.join(p['base_arts']) or '—'} | {p.get('base_trap', '')} |")
    L.append("\nRaw outputs (questions, drafts, quotes, rejected quotes, baseline answers) are in the run file.")
    (ROOT / "eval" / "results.md").write_text("\n".join(L) + "\n")

    pct = lambda a, n: round(100 * a / n) if n else 0  # noqa: E731
    mm = out["metrics"]
    web = {
        "chart": {
            "trap_refused": {"base": pct(mm["trap_refused"]["baseline"], mm["trap_refused"]["n"]), "belegt": pct(mm["trap_refused"]["belegt"], mm["trap_refused"]["n"])},
            "wrong_published": {"base": pct(mm["wrong_article_published"]["baseline"], mm["wrong_article_published"]["n"]), "belegt": pct(mm["wrong_article_published"]["belegt"], mm["wrong_article_published"]["n"])},
            "lang_agree": {"base": pct(mm["lang_agree"]["baseline"], mm["lang_agree"]["n"]), "belegt": pct(mm["lang_agree"]["belegt"], mm["lang_agree"]["n"])},
        },
        "table": [
            {"label": {"fr": "Article correct cité", "de": "Korrekter Artikel zitiert", "it": "Articolo corretto citato", "rm": "Artitgel correct cità", "en": "Correct article cited"}, **_pair(mm["correct_article"])},
            {"label": {"fr": "Article faux ou inventé publié", "de": "Falscher/erfundener Artikel veröffentlicht", "it": "Articolo errato o inventato pubblicato", "rm": "Artitgel fauss u inventà publitgà", "en": "Wrong or invented article published"}, **_pair(mm["wrong_article_published"])},
            {"label": {"fr": "Pièges refusés", "de": "Fallen abgelehnt", "it": "Trappole rifiutate", "rm": "Trappas refusadas", "en": "Traps refused"}, **_pair(mm["trap_refused"])},
            {"label": {"fr": "Abstention à tort", "de": "Fälschliche Enthaltung", "it": "Astensione errata", "rm": "Abstenziun sbagliada", "en": "Wrongful abstention"}, "base": "—", "belegt": _pair(mm["over_refusal"])["belegt"]},
            {"label": {"fr": "Même réponse dans les 4 langues", "de": "Gleiche Antwort in 4 Sprachen", "it": "Stessa risposta nelle 4 lingue", "rm": "Medema resposta en 4 linguas", "en": "Same answer in 4 languages"}, **_pair(mm["lang_agree"])},
        ] + ([{"label": {"fr": "Article correct — romanche", "de": "Korrekter Artikel — Rumantsch", "it": "Articolo corretto — romancio", "rm": "Artitgel correct — rumantsch", "en": "Correct article — Romansh"}, **_pair(mm["correct_rm"])}] if "correct_rm" in mm else []),
        "text": {
            "fr": f"{len(per)} questions ({len(ans)} avec réponse, {len(traps)} pièges), dont {len(groups)} posées dans les 4 langues. Même modèle Apertus 1.5 8B local, température 0. Intervalles de confiance à 95 % (Wilson).",
            "de": f"{len(per)} Fragen ({len(ans)} beantwortbar, {len(traps)} Fallen), davon {len(groups)} in allen 4 Sprachen. Gleiches lokales Modell Apertus 1.5 8B, Temperatur 0. 95-%-Konfidenzintervalle (Wilson).",
            "it": f"{len(per)} domande ({len(ans)} con risposta, {len(traps)} trappole), di cui {len(groups)} nelle 4 lingue. Stesso modello locale Apertus 1.5 8B, temperatura 0. Intervalli di confidenza al 95% (Wilson).",
            "rm": f"{len(per)} dumondas ({len(ans)} cun resposta, {len(traps)} trappas), da quellas {len(groups)} en tut las 4 linguas. Il medem model local Apertus 1.5 8B, temperatura 0.",
            "en": f"{len(per)} questions ({len(ans)} answerable, {len(traps)} traps), {len(groups)} of them asked in all 4 languages. Same local Apertus 1.5 8B model, temperature 0. 95% Wilson confidence intervals.",
        },
        "footnote": {
            "fr": "Détail par question, sorties brutes et étiquetage manuel des pièges : eval/results.md dans le dépôt.",
            "de": "Details pro Frage, Rohdaten und manuelle Kennzeichnung der Fallen: eval/results.md im Repository.",
            "it": "Dettagli per domanda, output grezzi ed etichette manuali delle trappole: eval/results.md nel repository.",
            "rm": "Detagls per dumonda: eval/results.md en il repository.",
            "en": "Per-question details, raw outputs and manual trap labels: eval/results.md in the repository.",
        },
    }
    (ROOT / "web" / "data").mkdir(parents=True, exist_ok=True)
    (ROOT / "web" / "data" / "eval-summary.json").write_text(json.dumps(web, ensure_ascii=False, indent=1))
    print("\n".join(L[:20]))


def _pair(v):
    return {"base": fmt(v["baseline"], v["n"]), "belegt": fmt(v["belegt"], v["n"])}


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else str(ROOT / "eval" / "runs" / "run.jsonl"))
