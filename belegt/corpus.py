"""Corpus: the Swiss Federal Constitution (SR 101) in DE, FR, IT and RM.

The official Akoma Ntoso XML published on fedlex.admin.ch is converted into a
flat list of *paragraphs*. Every paragraph keeps the official Fedlex eId
(e.g. ``art_22/para_1``). Because the eIds are identical in the four language
versions, the same provision can be lined up across languages without any
machine translation: this is what makes the cross-language check exact.
"""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
import xml.etree.ElementTree as ET
from dataclasses import dataclass, asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FEDLEX_DIR = ROOT / "data" / "fedlex"
CORPUS_DIR = ROOT / "data" / "corpus"

LANGS = ("de", "fr", "it", "rm")
VERSION = "20240303"
ELI = "https://fedlex.data.admin.ch/eli/cc/1999/404"
FEDLEX_URL = {
    "de": "https://www.fedlex.admin.ch/eli/cc/1999/404/de",
    "fr": "https://www.fedlex.admin.ch/eli/cc/1999/404/fr",
    "it": "https://www.fedlex.admin.ch/eli/cc/1999/404/it",
    "rm": "https://www.fedlex.admin.ch/eli/cc/1999/404/rm",
}
NS = "{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}"


@dataclass
class Paragraph:
    id: str            # Fedlex eId, identical across languages: "art_22/para_1"
    article: str       # "art_22"
    label: str         # "Art. 22 al. 1" / "Art. 22 Abs. 1" / ...
    art_num: str       # "22"
    para_num: str      # "1" or ""
    heading: str       # article heading in that language
    text: str          # paragraph text, notes stripped

    def to_dict(self):
        return asdict(self)


PARA_WORD = {"de": "Abs.", "fr": "al.", "it": "cpv.", "rm": "al."}


def _tag(el) -> str:
    return el.tag.replace(NS, "")


def _text(el) -> str:
    """Visible text of an element, without authorial notes (footnotes)."""
    out = []

    def walk(e):
        t = _tag(e)
        if t == "authorialNote":
            if e.tail:
                out.append(e.tail)
            return
        if t in ("num",) and e is not el:
            # list item numbers ("a.", "b.") are kept, they are part of the text
            pass
        if e.text:
            out.append(e.text)
        for c in e:
            walk(c)
            if t in ("blockList",) and _tag(c) in ("item", "listIntroduction"):
                out.append(" ")
        if e is not el and e.tail:
            out.append(e.tail)

    walk(el)
    s = "".join(out)
    s = s.replace(" ", " ")
    s = re.sub(r"\s+", " ", s).strip()
    # remove the footnote star used by Fedlex in some headings
    s = re.sub(r"\s*\*$", "", s)
    return s


def _art_num(article_el) -> str:
    num = article_el.find(f"{NS}num")
    if num is None:
        return ""
    t = _text(num)
    m = re.search(r"(\d+[a-z]*(?:\s?(?:bis|ter|quater|quinquies|sexies|septies|octies|novies|decies))?)", t)
    return m.group(1).replace(" ", "") if m else t


def parse_language(lang: str) -> list[Paragraph]:
    path = FEDLEX_DIR / f"sr101-{VERSION}-{lang}.xml"
    tree = ET.parse(path)
    body = tree.getroot().find(f".//{NS}body")
    paras: list[Paragraph] = []
    for art in body.iter(f"{NS}article"):
        aid = art.get("eId")
        anum = _art_num(art)
        h = art.find(f"{NS}heading")
        heading = _text(h) if h is not None else ""
        for p in art.iter(f"{NS}paragraph"):
            pid = p.get("eId")
            n = p.find(f"{NS}num")
            pnum = _text(n) if n is not None else ""
            content = p.find(f"{NS}content")
            if content is None:
                continue
            text = _text(content)
            if len(text.strip(" .…")) < 3:   # repealed paragraph ("…")
                continue
            # sub-heading of transitional provisions (art. 197 ch. 2 ...)
            sub_heading = ""
            for sub in art.iter(f"{NS}subdivision"):
                if p in list(sub.iter(f"{NS}paragraph")):
                    sh = sub.find(f"{NS}heading")
                    sub_heading = _text(sh) if sh is not None else ""
                    break
            label = f"Art. {anum}"
            if pnum:
                label += f" {PARA_WORD[lang]} {pnum}"
            paras.append(Paragraph(
                id=pid, article=aid, label=label, art_num=anum, para_num=pnum,
                heading=(heading + (" — " + sub_heading if sub_heading else "")),
                text=text,
            ))
    return paras


def build() -> dict:
    CORPUS_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {"sr": "101", "eli": ELI, "version": VERSION, "languages": {}}
    for lang in LANGS:
        paras = parse_language(lang)
        out = CORPUS_DIR / f"{lang}.json"
        out.write_text(json.dumps([p.to_dict() for p in paras], ensure_ascii=False, indent=0))
        src = FEDLEX_DIR / f"sr101-{VERSION}-{lang}.xml"
        manifest["languages"][lang] = {
            "paragraphs": len(paras),
            "articles": len({p.article for p in paras}),
            "source_xml": src.name,
            "source_sha256": hashlib.sha256(src.read_bytes()).hexdigest(),
            "corpus_sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
            "url": FEDLEX_URL[lang],
        }
    (CORPUS_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2))
    return manifest


class Corpus:
    """In-memory, four-language corpus aligned on Fedlex eIds."""

    def __init__(self):
        self.manifest = json.loads((CORPUS_DIR / "manifest.json").read_text())
        self.by_lang: dict[str, list[dict]] = {}
        self.index: dict[str, dict[str, dict]] = {}
        for lang in LANGS:
            rows = json.loads((CORPUS_DIR / f"{lang}.json").read_text())
            self.by_lang[lang] = rows
            self.index[lang] = {r["id"]: r for r in rows}
        self.ids = [r["id"] for r in self.by_lang["de"]]

    def get(self, lang: str, pid: str) -> dict | None:
        return self.index[lang].get(pid)

    def article_paragraphs(self, lang: str, article: str) -> list[dict]:
        return [r for r in self.by_lang[lang] if r["article"] == article]

    def parallel(self, pid: str) -> dict[str, dict | None]:
        return {lang: self.index[lang].get(pid) for lang in LANGS}

    def fingerprint(self) -> str:
        h = hashlib.sha256()
        for lang in LANGS:
            h.update(self.manifest["languages"][lang]["corpus_sha256"].encode())
        return h.hexdigest()


def normalize(s: str) -> str:
    """Normalisation used by the verifier: typographic quotes/apostrophes,
    dashes, whitespace and Unicode composition. Nothing semantic."""
    s = unicodedata.normalize("NFC", s)
    s = (s.replace("’", "'").replace("‘", "'").replace("`", "'")
           .replace("«", '"').replace("»", '"').replace("“", '"').replace("”", '"')
           .replace("„", '"').replace("‹", "'").replace("›", "'")
           .replace("–", "-").replace("—", "-").replace(" ", " "))
    s = re.sub(r"\s+", " ", s).strip()
    return s


if __name__ == "__main__":
    m = build()
    print(json.dumps(m, indent=2))
