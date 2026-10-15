"""Belegt pipeline: understand -> retrieve (4 languages) -> draft -> verify -> receipt.

Who does what:
  * Apertus (AI)      understands the question, rewrites it in the four
                      official languages, drafts an answer and picks quotes.
  * Deterministic code retrieves candidate paragraphs, checks every quote
                      verbatim against the official text, removes unproven
                      claims, checks cross-language agreement, and decides
                      to publish or to abstain.
"""
from __future__ import annotations

import hashlib
import json
import time
import uuid
from datetime import datetime, timezone

from . import llm
from .corpus import LANGS, Corpus
from .retrieve import Retriever, detect_language
from .verify import verify

LANG_NAME = {"de": "German", "fr": "French", "it": "Italian", "rm": "Romansh (Rumantsch Grischun)", "en": "English"}
TOP_K = 6

UNDERSTAND_SCHEMA = {
    "type": "object",
    "properties": {
        "de": {"type": "string", "maxLength": 160},
        "fr": {"type": "string", "maxLength": 160},
        "it": {"type": "string", "maxLength": 160},
        "rm": {"type": "string", "maxLength": 160},
        "keywords": {"type": "array", "items": {"type": "string", "maxLength": 40}, "maxItems": 6},
    },
    "required": ["de", "fr", "it", "rm", "keywords"],
}
UNDERSTAND_SYS = (
    "You prepare search queries for the Swiss Federal Constitution. Given a citizen's question, "
    "rewrite it as a short search query in each official language (German de, French fr, Italian it, "
    "Romansh rm), using the legal vocabulary the Constitution itself would use "
    "(e.g. 'demonstrate in the street' -> 'freedom of assembly'; 'vote at 18' -> 'political rights, age'). "
    "Also give up to 6 legal keywords in the question's language. Do not write 'article' or 'Art.': name the legal topic. "
    "Never answer the question. Output compact JSON only."
)

ANSWER_SCHEMA = {
    "type": "object",
    "properties": {
        "answerable": {"type": "boolean"},
        "answer": {"type": "string", "maxLength": 700},
        "citations": {
            "type": "array",
            "maxItems": 3,
            "items": {
                "type": "object",
                "properties": {"source": {"type": "string", "enum": [f"S{i}" for i in range(1, TOP_K + 1)]},
                               "quote": {"type": "string", "maxLength": 400}},
                "required": ["source", "quote"],
            },
        },
    },
    "required": ["answerable", "answer", "citations"],
}


def answer_system(lang: str) -> str:
    return (
        "You are Belegt, a careful assistant for the Swiss Federal Constitution. Rule: cite or stay silent.\n"
        "You receive a question and numbered sources S1..S6, which are paragraphs of the official text.\n"
        "1. Decide whether the sources DIRECTLY answer the question. If they do not, or only touch the topic, "
        "set answerable=false, write one short sentence saying no provision answers this, and give no citations.\n"
        "2. If they do, set answerable=true and write a plain answer of 1 to 3 short sentences in "
        f"{LANG_NAME[lang]}. Do not add facts that are not in the sources. Do not give legal advice.\n"
        "3. For each claim, add a citation: the source id and a quote copied EXACTLY, character for character, "
        "from that source (one full sentence or clause, at least 5 words). Never paraphrase inside a quote.\n"
        "4. Only mention article numbers that appear in the sources you cite.\n"
        "Output JSON only."
    )


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _sha(s: str | bytes) -> str:
    if isinstance(s, str):
        s = s.encode()
    return hashlib.sha256(s).hexdigest()


class Belegt:
    def __init__(self, model_sha256: callable = lambda: None, network_state: callable = lambda: {}):
        self.corpus = Corpus()
        self.retriever = Retriever(self.corpus)
        self.model_sha256 = model_sha256
        self.network_state = network_state

    # ---------------------------------------------------------------- steps
    def understand(self, question: str) -> dict:
        r = llm.chat(
            [{"role": "system", "content": UNDERSTAND_SYS}, {"role": "user", "content": question}],
            schema=UNDERSTAND_SCHEMA, max_tokens=260,
        )
        try:
            data = json.loads(r["text"])
        except json.JSONDecodeError:
            data = {}
        return {"queries": {l: (data.get(l) or "") for l in LANGS}, "keywords": data.get("keywords") or [],
                "seconds": r["seconds"], "raw": r["text"]}

    def retrieve(self, question: str, q_lang: str, understood: dict) -> dict:
        queries = {}
        for l in LANGS:
            q = understood["queries"].get(l, "")
            if l == q_lang:
                q = question + " " + q + " " + " ".join(understood.get("keywords", []))
            queries[l] = q.strip() or question
        return self.retriever.search(queries, k=TOP_K)

    def draft(self, question: str, ev_lang: str, ans_lang: str, ids: list[str]) -> dict:
        lines = []
        for i, pid in enumerate(ids, 1):
            p = self.corpus.get(ev_lang, pid)
            lines.append(f"S{i} [{p['label']} — {p['heading']}]: {p['text']}")
        user = "Question: " + question + "\n\nSources:\n" + "\n".join(lines)
        messages = [{"role": "system", "content": answer_system(ans_lang)}, {"role": "user", "content": user}]
        r = llm.chat(messages, schema=ANSWER_SCHEMA, max_tokens=420)
        try:
            data = json.loads(r["text"])
        except json.JSONDecodeError:
            data = {"answerable": False, "answer": "", "citations": []}
        cits = []
        for c in data.get("citations", []):
            try:
                idx = int(str(c.get("source", "S0"))[1:]) - 1
            except ValueError:
                continue
            if 0 <= idx < len(ids):
                cits.append({"id": ids[idx], "quote": c.get("quote", ""), "source": c.get("source")})
        return {"answerable": bool(data.get("answerable")), "answer": data.get("answer", ""),
                "citations": cits, "seconds": r["seconds"], "raw": r["text"],
                "prompt_sha256": _sha(json.dumps(messages, ensure_ascii=False)), "timings": r.get("timings", {})}

    # ------------------------------------------------------------- pipeline
    def run(self, question: str, lang_hint: str | None = None):
        """Generator of events: {'type': 'step'|'result', ...}"""
        t0 = time.time()
        q_lang = lang_hint if lang_hint in (*LANGS, "en") else detect_language(question)
        ev_lang = q_lang if q_lang in LANGS else "fr"
        yield {"type": "step", "step": "detect", "status": "done", "lang": q_lang}

        yield {"type": "step", "step": "understand", "status": "start"}
        und = self.understand(question)
        yield {"type": "step", "step": "understand", "status": "done", "seconds": und["seconds"],
               "queries": und["queries"], "keywords": und["keywords"]}

        yield {"type": "step", "step": "retrieve", "status": "start"}
        t = time.time()
        ret = self.retrieve(question, q_lang, und)
        ids = [pid for pid, _ in ret["fused"]][:TOP_K]
        yield {"type": "step", "step": "retrieve", "status": "done", "seconds": round(time.time() - t, 2),
               "candidates": [self.corpus.get(ev_lang, i)["label"] for i in ids]}

        yield {"type": "step", "step": "draft", "status": "start"}
        dr = self.draft(question, ev_lang, q_lang, ids)
        yield {"type": "step", "step": "draft", "status": "done", "seconds": dr["seconds"]}

        yield {"type": "step", "step": "verify", "status": "start"}
        t = time.time()
        if dr["answerable"]:
            ver = verify(self.corpus, ev_lang, dr["answer"], dr["citations"], allowed_ids=set(ids))
        else:
            ver = {"ok": False, "answer": "", "verified": [], "rejected": [], "removed_sentences": [], "sentences": [],
                   "checks": [{"rule": "R5", "name": "citation_or_silence", "passed": True,
                               "detail": "model found no direct answer: abstained"}]}
        # cross-language agreement: does independent retrieval in each language reach the cited articles?
        consistency = []
        for v in ver["verified"]:
            found = {l: (v["article"] in ret["per_lang_articles"].get(l, [])) for l in LANGS}
            consistency.append({"id": v["id"], "article": v["article"], "found_in": found,
                                "agree": sum(found.values())})
        cons_ok = all(c["agree"] == len(LANGS) for c in consistency) if consistency else None
        ver["checks"].append({"rule": "X", "name": "cross_language_agreement",
                              "passed": cons_ok if cons_ok is not None else True,
                              "detail": "; ".join(f"{c['article']}: {c['agree']}/4" for c in consistency) or "n/a"})
        yield {"type": "step", "step": "verify", "status": "done", "seconds": round(time.time() - t, 3)}

        decision = "answered" if ver["ok"] else "abstained"
        nearest = []
        seen = set()
        for pid in ids:
            p = self.corpus.get(ev_lang, pid)
            if p["article"] in seen:
                continue
            seen.add(p["article"])
            nearest.append({"article": p["article"], "label": f"Art. {p['art_num']}", "heading": p["heading"], "id": pid})
            if len(nearest) == 3:
                break

        parallel = {}
        for v in ver["verified"]:
            parallel[v["id"]] = {l: self.corpus.get(l, v["id"]) for l in LANGS}

        receipt = self.receipt(question, q_lang, ev_lang, und, ret, ids, dr, ver, consistency, decision, t0)
        yield {
            "type": "result",
            "decision": decision,
            "lang": q_lang,
            "evidence_lang": ev_lang,
            "answer": ver["answer"],
            "model_said_answerable": dr["answerable"],
            "model_answer_raw": dr["answer"],
            "model_citations_raw": dr["citations"],
            "timings": {"understand": und["seconds"], "draft": dr["seconds"]},
            "citations": ver["verified"],
            "rejected": ver["rejected"],
            "removed_sentences": ver["removed_sentences"],
            "sentences": ver["sentences"],
            "consistency": consistency,
            "consistency_ok": cons_ok,
            "per_lang_articles": ret["per_lang_articles"],
            "nearest": nearest,
            "parallel": parallel,
            "checks": ver["checks"],
            "receipt": receipt,
            "seconds": round(time.time() - t0, 2),
        }

    # -------------------------------------------------------------- receipt
    def receipt(self, question, q_lang, ev_lang, und, ret, ids, dr, ver, consistency, decision, t0) -> dict:
        m = self.corpus.manifest
        body = {
            "format": "belegt-receipt/1",
            "issued_at": _now(),
            "question_sha256": _sha(question),
            "question": question,
            "language": q_lang,
            "decision": decision,
            "model": {"name": llm.MODEL_NAME, "file": llm.MODEL_FILE, "sha256": self.model_sha256(),
                      "runtime": "llama.cpp (local, CPU)", "endpoint": llm.LLM_URL,
                      "temperature": 0, "seed": 42},
            "law": {"title": "Federal Constitution of the Swiss Confederation", "sr": m["sr"], "eli": m["eli"],
                    "version": m["version"], "evidence_language": ev_lang,
                    "text_sha256": m["languages"][ev_lang]["corpus_sha256"],
                    "source_xml_sha256": m["languages"][ev_lang]["source_sha256"]},
            "retrieval": {"queries": und["queries"], "candidates": ids,
                          "per_language_top_articles": ret["per_lang_articles"]},
            "evidence": [{"id": v["id"], "label": v["label"], "quote": v["quote"], "span": v["span"],
                          "quote_sha256": _sha(v["quote"]), "verified": True} for v in ver["verified"]],
            "rejected_quotes": [{"id": r.get("id"), "reason": r["reason"]} for r in ver["rejected"]],
            "removed_sentences": ver["removed_sentences"],
            "checks": ver["checks"],
            "cross_language": consistency,
            "prompt_sha256": dr["prompt_sha256"],
            "model_output_sha256": _sha(dr["raw"]),
            "network": self.network_state(),
            "duration_seconds": round(time.time() - t0, 2),
        }
        body["receipt_id"] = "BLG-" + _sha(json.dumps(body, ensure_ascii=False, sort_keys=True))[:12].upper()
        return body
