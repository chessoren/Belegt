"""Lexical retrieval, pure Python, no external service.

Two BM25 indexes per language are fused with reciprocal-rank fusion:
  * a word index (light normalisation, stop words removed),
  * a character 5-gram index, robust to German compounds
    ("Versammlungsfreiheit") and to Romansh morphology.

Retrieval is *not* where trust comes from in Belegt: it only proposes
candidate paragraphs. Trust comes from the verifier (see verify.py).
"""
from __future__ import annotations

import math
import re
import unicodedata
from collections import Counter, defaultdict

from .corpus import LANGS, Corpus

STOP = {
    "de": "der die das den dem des ein eine einer eines einem einen und oder aber ich du er sie es wir ihr mich mir dich dir sich ist sind war waren bin bist hat habe haben hatte wird werden wurde kann können darf dürfen muss müssen soll sollen in im ins an am auf aus bei mit nach von vom zu zum zur für über unter durch gegen ohne um was wie wer wo wann warum welche welcher welches nicht kein keine auch nur noch schon so dass ob als wenn mein meine dein deine sein seine man es gibt etwa bitte gilt schweiz schweizer bundesverfassung verfassung artikel art",
    "fr": "le la les l un une des du de d et ou mais je tu il elle on nous vous ils elles me te se moi toi lui leur leurs est sont été être suis es a ai as avons avez ont avoir peut peux puis pouvons pouvez peuvent dois doit doivent faut dans en au aux sur sous par pour avec sans chez que qui quoi quel quelle quels quelles quand comment où pourquoi ne pas plus ni ce cet cette ces mon ma mes ton ta tes son sa ses y si est-ce qu c s n j m t droit suisse constitution fédérale article art",
    "it": "il lo la i gli le l un uno una di del della dei degli delle da dal dalla in nel nella su sul per con tra fra e ed o ma io tu lui lei noi voi loro mi ti si ci è sono essere ho hai ha abbiamo avete hanno posso può possono devo deve devono che chi cosa quale quali quando come dove perché non più anche se mio mia tuo tua suo sua c diritto svizzera costituzione federale articolo art",
    "rm": "il la ils las l in ina d da dal da la dals e ed u ma jau ti el ella nus vus els ellas ma mi ta tes sia ses è èn esser sun es hai has ha avain avais han poss pos po pudain pudais pon stoss sto ston che tge tgi tgenin cura co nua pertge betg nagin naginas er sche sco quai quel quella cun per sin sur tar tras senza ord en davent dretg svizra constituziun federala artitgel art",
    "en": "the a an of to in on at for with by from and or but i you he she it we they me my your his her its our their is are was were be been am do does did have has had can could may might must shall should will would what which who whom when where why how not no any some this that these those there here if as into about switzerland swiss constitution federal article art",
}
STOP = {k: set(v.split()) for k, v in STOP.items()}

# Words that strongly signal one language over the others (for detection).
MARKERS = {
    "rm": set("betg èn ils dals tge tgi pertge nua mintga quai hai avain dretg svizra pievel chantun chantuns lescha vegn vegnan pon dastgel dastg sun jau persuna".split()),
    "it": set("il gli della delle dei degli che non sono è ho posso diritto svizzera legge cittadini perché dove come può chi".split()),
    "fr": set("le les des est sont je ai puis droit suisse loi qui que pas une peut quel quelle est-ce pourquoi où ont".split()),
    "de": set("der die das und ist ich nicht ein eine darf kann recht schweiz gesetz wer wie was warum welche muss gibt".split()),
    "en": set("the is are what can do does my right law who how why which there have".split()),
}


def strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


WORD_RE = re.compile(r"[a-zà-öø-ÿ0-9]+", re.I)


def words(text: str) -> list[str]:
    text = text.lower().replace("’", "'")
    return WORD_RE.findall(text)


def stem(w: str) -> str:
    # deliberately crude, language-agnostic suffix trimming
    w = strip_accents(w)
    for suf in ("ungen", "ungs", "heit", "keit", "ement", "ements", "ation", "ations", "azione", "azioni",
                "aziun", "aziuns", "ions", "ion", "ung", "ens", "ern", "en", "es", "er", "e", "s", "i", "a", "o"):
        if len(w) > len(suf) + 3 and w.endswith(suf):
            return w[: -len(suf)]
    return w


def word_tokens(text: str, lang: str) -> list[str]:
    stop = STOP.get(lang, set())
    return [stem(w) for w in words(text) if w not in stop and len(w) > 1]


def char_tokens(text: str, lang: str, n: int = 5) -> list[str]:
    stop = STOP.get(lang, set())
    out = []
    for w in words(text):
        if w in stop:
            continue
        w = strip_accents(w)
        if len(w) <= n:
            out.append(w)
            continue
        for i in range(len(w) - n + 1):
            out.append(w[i:i + n])
    return out


def detect_language(text: str) -> str:
    ws = [w.lower() for w in words(text)]
    if not ws:
        return "fr"
    score = {lang: sum(1 for w in ws if w in MARKERS[lang]) for lang in MARKERS}
    # Romansh-specific characters / clusters
    t = text.lower()
    if re.search(r"\b(betg|èn|tge|tgi|pertge)\b", t) or "tsch" in t or "dretg" in t:
        score["rm"] += 2
    if re.search(r"[äöüß]", t):
        score["de"] += 1
    best = max(score, key=lambda k: (score[k], k == "fr"))
    return best if score[best] > 0 else "fr"


class BM25:
    def __init__(self, docs: list[list[str]], k1: float = 1.4, b: float = 0.72):
        self.k1, self.b = k1, b
        self.N = len(docs)
        self.len = [len(d) for d in docs]
        self.avg = sum(self.len) / max(1, self.N)
        self.tf = [Counter(d) for d in docs]
        df = Counter()
        for d in self.tf:
            df.update(d.keys())
        self.idf = {t: math.log(1 + (self.N - n + 0.5) / (n + 0.5)) for t, n in df.items()}
        self.post = defaultdict(list)
        for i, d in enumerate(self.tf):
            for t in d:
                self.post[t].append(i)

    def scores(self, q: list[str]) -> dict[int, float]:
        s: dict[int, float] = defaultdict(float)
        for t in set(q):
            idf = self.idf.get(t)
            if idf is None:
                continue
            for i in self.post[t]:
                f = self.tf[i][t]
                s[i] += idf * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * self.len[i] / self.avg))
        return s


class Retriever:
    def __init__(self, corpus: Corpus):
        self.corpus = corpus
        self.word: dict[str, BM25] = {}
        self.char: dict[str, BM25] = {}
        for lang in LANGS:
            rows = corpus.by_lang[lang]
            docs = [r["heading"] + " " + r["heading"] + " " + r["text"] for r in rows]
            self.word[lang] = BM25([word_tokens(d, lang) for d in docs])
            self.char[lang] = BM25([char_tokens(d, lang) for d in docs])

    def search_lang(self, query: str, lang: str, k: int = 20) -> list[tuple[str, float]]:
        """Ranked paragraph ids for one language (word+char BM25, RRF fused)."""
        rows = self.corpus.by_lang[lang]
        sw = self.word[lang].scores(word_tokens(query, lang))
        sc = self.char[lang].scores(char_tokens(query, lang))
        fused: dict[int, float] = defaultdict(float)
        for s in (sw, sc):
            for rank, (i, _) in enumerate(sorted(s.items(), key=lambda x: -x[1])[:100]):
                fused[i] += 1.0 / (60 + rank)
        best = sorted(fused.items(), key=lambda x: -x[1])[:k]
        return [(rows[i]["id"], v) for i, v in best]

    def search(self, queries: dict[str, str], k: int = 8) -> dict:
        """queries: {lang: question in that language}. Returns fused ranking
        across languages plus each language's own top articles."""
        per_lang = {lang: self.search_lang(q, lang, k=30) for lang, q in queries.items() if q}
        fused: dict[str, float] = defaultdict(float)
        for lang, ranked in per_lang.items():
            for rank, (pid, _) in enumerate(ranked):
                fused[pid] += 1.0 / (60 + rank)
        ranked = sorted(fused.items(), key=lambda x: -x[1])
        top_articles = {}
        for lang, ranked_l in per_lang.items():
            arts = []
            for pid, _ in ranked_l:
                a = pid.split("/")[0]
                if a not in arts:
                    arts.append(a)
                if len(arts) == 5:
                    break
            top_articles[lang] = arts
        return {
            "fused": [(pid, round(s, 5)) for pid, s in ranked[:k]],
            "per_lang_articles": top_articles,
        }
