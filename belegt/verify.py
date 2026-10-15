"""The verifier. No AI in here: plain, deterministic string checks.

Rules ("citation ou silence"):
  R1  Every citation must point to a paragraph that exists in the official text.
  R2  Every quote must appear *verbatim* in that paragraph (only typographic
      normalisation: quotes, apostrophes, dashes, whitespace).
  R3  Quotes must be long enough to carry meaning (>= MIN_QUOTE chars).
  R4  Any article number mentioned in the answer must be one of the verified
      citations. A sentence that names an unproven article is removed.
  R5  If no citation survives, nothing is asserted: Belegt abstains.
"""
from __future__ import annotations

import re

from .corpus import Corpus, normalize

MIN_QUOTE = 15
ART_RE = re.compile(
    r"\b(?:art(?:\.|icle|ikel|icolo|itgel)?s?)\s*(\d{1,3}\s?[a-z]?(?:bis|ter|quater|quinquies|sexies|septies|octies|novies|decies)?)\b",
    re.I,
)
SENT_RE = re.compile(r"(?<=[.!?;])\s+(?=[A-ZÀ-ÖØ-Þ«\"“„(])")


def _clean_quote(q: str) -> str:
    q = normalize(q)
    q = q.strip(" \"'")
    q = re.sub(r"^(\.\.\.|…)\s*", "", q)
    q = re.sub(r"\s*(\.\.\.|…)$", "", q)
    return q.rstrip(" .;:,")


def locate(quote: str, paragraph_text: str) -> tuple[int, int] | None:
    """Character span of the quote inside the *normalized* paragraph text."""
    q = _clean_quote(quote)
    t = normalize(paragraph_text)
    if len(q) < MIN_QUOTE:
        return None
    i = t.find(q)
    if i < 0:
        # case-insensitive fallback only for the first character (sentence case)
        i = t.lower().find(q.lower())
        if i < 0:
            return None
    return (i, i + len(q))


def split_sentences(text: str) -> list[str]:
    text = text.strip()
    if not text:
        return []
    return [s.strip() for s in SENT_RE.split(text) if s.strip()]


def art_numbers(text: str) -> set[str]:
    return {m.group(1).replace(" ", "").lower() for m in ART_RE.finditer(text)}


def _grams(text: str, n: int = 5) -> set[str]:
    t = re.sub(r"[^\w]+", " ", normalize(text).lower())
    out = set()
    for w in t.split():
        if len(w) < 4:
            continue
        out.update(w[i:i + n] for i in range(max(1, len(w) - n + 1)))
    return out


def support(sentence: str, evidence: str) -> dict:
    """How much of a sentence is literally backed by the cited text.
    A transparency signal shown to the reader, not a truth detector."""
    g = _grams(sentence)
    if not g:
        return {"score": 1.0, "kind": "quoted"}
    score = len(g & _grams(evidence)) / len(g)
    kind = "quoted" if score >= 0.6 else ("paraphrase" if score >= 0.35 else "inference")
    return {"score": round(score, 2), "kind": kind}


def verify(corpus: Corpus, lang: str, answer: str, citations: list[dict], allowed_ids: set[str] | None = None) -> dict:
    checks = []
    verified, rejected = [], []
    for c in citations:
        pid = (c.get("id") or "").strip()
        quote = c.get("quote") or ""
        para = corpus.get(lang, pid)
        if para is None:
            rejected.append({**c, "reason": "R1: paragraph does not exist"})
            continue
        if allowed_ids is not None and pid not in allowed_ids:
            rejected.append({**c, "reason": "R1: paragraph was not among the retrieved sources"})
            continue
        span = locate(quote, para["text"])
        if span is None:
            reason = "R3: quote too short" if len(_clean_quote(quote)) < MIN_QUOTE else "R2: quote not found verbatim"
            rejected.append({**c, "reason": reason, "label": para["label"]})
            continue
        if any(v["id"] == pid and v["span"] == list(span) for v in verified):
            continue
        verified.append({
            "id": pid, "label": para["label"], "article": para["article"], "art_num": para["art_num"],
            "heading": para["heading"], "quote": normalize(para["text"])[span[0]:span[1]],
            "para_text": para["text"],
            "span": list(span), "lang": lang,
        })
    checks.append({"rule": "R1-R3", "name": "verbatim_quotes",
                   "passed": len(verified) > 0,
                   "detail": f"{len(verified)} verified, {len(rejected)} rejected"})

    proven_arts = {v["art_num"].lower() for v in verified}
    kept, removed = [], []
    for s in split_sentences(answer):
        unproven = art_numbers(s) - proven_arts
        if unproven:
            removed.append({"sentence": s, "reason": "R4: mentions unproven article " + ", ".join(sorted(unproven))})
        else:
            kept.append(s)
    checks.append({"rule": "R4", "name": "no_unproven_article_numbers",
                   "passed": not removed, "detail": f"{len(removed)} sentence(s) removed"})

    final_answer = " ".join(kept).strip()
    evidence_text = " ".join(corpus.get(lang, v["id"])["text"] for v in verified)
    sentences = [{"text": s, "support": support(s, evidence_text)} for s in kept] if verified else []
    ok = bool(verified) and bool(final_answer)
    checks.append({"rule": "R5", "name": "citation_or_silence", "passed": True,
                   "detail": "answer published" if ok else "abstained"})
    return {
        "ok": ok,
        "answer": final_answer if ok else "",
        "verified": verified,
        "rejected": rejected,
        "removed_sentences": removed,
        "sentences": sentences,
        "checks": checks,
    }
