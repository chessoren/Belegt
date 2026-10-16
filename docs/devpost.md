# Belegt — Devpost submission kit

> Generated from `docs/devpost.template.md` by `scripts/fill_numbers.py`. Every number below comes from `eval/summary.json` (run `eval/runs/run.jsonl`).
> Note: the Devpost page says final submissions for Hack Apertus are handled on **https://hackapertus.ch/online-hack/submissions** — submit there as well as on Devpost.

---

## Project name (title)

**Belegt**

## Tagline / subtitle (≤ 200 characters)

**Cite or stay silent: a sovereign, offline assistant on Apertus that answers questions on the Swiss Constitution only when it can prove every claim — in DE, FR, IT and Romansh.**

Shorter alternative (≤ 60): *Swiss law, proven word for word — or not answered at all.*

## Track / prize to select

- Track: **2B — Apertus Adoption: Own Project**
- Sponsor / Special prizes: tick **Hack Apertus Online – Winner Apertus Adoption: Own project** (the 1st and 2nd runner-up of the same track can also be ticked; they are the same category).
- Optional mention in the text: findings feed Track 1A (red-teaming: failures of Apertus alone) and 1B (Swiss Voices: cross-language divergences, Romansh).

## 25 tags ("Built with" / keywords)

apertus · swiss-ai · llama.cpp · gguf · python · retrieval-augmented-generation · bm25 · fedlex · akoma-ntoso · swiss-constitution · legal-tech · govtech · sovereign-ai · offline-first · trustworthy-ai · hallucination-detection · grounding · citations · multilingual · romansh · rumantsch · evaluation · audit-trail · open-source · design-system

## Elevator pitch (short description field)

AI assistants answer with confidence even when they are wrong. On our test set, Apertus asked alone named a wrong or invented article of the Swiss Constitution in **59%** of answers. Belegt, built on Apertus, does the opposite: it answers only with sentences that a deterministic verifier finds **word for word** in the official Fedlex text, checks that the four language versions agree, issues a receipt for every answer, and otherwise stays silent. With Belegt, wrong or invented articles dropped to **5%**, on the same local model, fully offline.

## Video demo

- Main cut: `docs/video/Belegt-demo.mp4` (1:30) — French voice-over (Oren, Fish Audio s2.1-pro-free), burned-in FR + EN subtitles (`.srt` alongside).
- Extended cut: `docs/video/Belegt-demo-extended.mp4` (≈ 2:00) with more explanation.
- Upload to YouTube/Vimeo (unlisted) and paste the link.

Suggested video description: *All app footage is the real application, recorded live inside a Linux network namespace with no route out (routing table empty, 0 outbound connections shown in the header). The local model's thinking time is time-lapsed and marked “accéléré ×N” on screen; screen recording slowed the CPU, the measured median latency without recording is 49.2 s per answer on 4 cores. The opening examples are real outputs of Apertus 1.5 8B asked alone (eval items t01 and q02).*

## Try it out / links

- Code: https://github.com/chessoren/swiss (branch `claude/america-gov-swiss-design-xalzfq` until merged)
- Run: `scripts/start.sh` → http://127.0.0.1:8080 · offline proof: `sudo scripts/offline_demo.sh`

## Image gallery

`docs/deck/png/slide-01.png` … `slide-14.png` (3:2, 2400×1600) and `docs/img/*.png` (UI screenshots).

---

## About the project (Devpost story — Markdown)

### Inspiration

The main brake on AI in the public sector is not power or price. It is trust. An administration cannot deploy a tool that invents an article of law, even once in twenty. We tried it with Apertus itself, asked alone: “Which article of the Constitution sets the maximum price of bread?” — *“Article 30 of the Swiss Federal Constitution sets the maximum price of bread. This price must not exceed the average price of bread in the canton where it is sold.”* No such provision exists. “What are the national languages?” — *“German, French and Italian.”* Romansh, forgotten. Fluent, plausible, wrong: exactly the failure a citizen can’t detect. Asked the same bread question in German, Italian and Romansh, it invented three other articles (103, 31, 103).

A disclaimer like “please verify” moves the burden to the user. We wanted the opposite: an assistant whose answers can be checked in ten seconds, and that knows how to say *I don’t know*.

### What it does

Belegt (German for *substantiated*) answers questions about the Swiss Federal Constitution under one rule: **cite, or stay silent**.

- **Proven.** Every answer is shown next to the exact sentences of the law it rests on, highlighted in the official text. One click opens the article in German, French, Italian or Romansh.
- **Honest.** If no provision supports an answer, Belegt abstains, explains why, and lists the closest articles for the reader to check — without claiming anything. *“Which article sets the maximum price of bread?”* → none, and it says so.
- **One law, four languages.** Ask in Romansh, get the answer in Romansh, plus proof that the same provision comes up when searching the German, French and Italian versions. Divergences are flagged instead of silently resolved.
- **A receipt for every answer.** Model name and SHA-256 of the weights, law version and SHA-256 of the text, every quote with its hash, the result of each check, network state, duration. Downloadable, printable, fileable by a legal or compliance team.
- **Sovereign, demonstrated.** Apertus runs on the machine (llama.cpp, CPU). Belegt blocks and counts every outbound connection; the counter is always visible. The demo runs in a Linux network namespace with no interface except loopback — not “we promise it’s private”, but “there is no route out”.

What it is not: a legal adviser. It helps people find and read the official text.

### How we built it

**Who does what** is the core of the design:

1. **Apertus (AI) understands.** It rewrites the citizen’s question in the four official languages using the Constitution’s vocabulary (*“demonstrate in the street”* → *“freedom of assembly / Versammlungsfreiheit / libertà di riunione / libertad da reuniun”*). Output is JSON constrained by a llama.cpp grammar.
2. **Code searches.** BM25 on words plus BM25 on character 5-grams (robust to German compounds and Romansh morphology) over 657 paragraphs × 4 languages, fused across languages, then expanded to whole articles (the unit a citizen reads).
3. **Apertus drafts.** 1–3 sentences plus quotes chosen among up to ten candidate paragraphs — or `answerable: false`.
4. **Code verifies, no AI involved.** R1 the paragraph exists · R2 the quote appears word for word (only typographic normalisation) · R3 it is long enough · R4 any article number in the answer must be among the verified citations, otherwise the sentence is removed · R5 if no evidence survives, abstain · X independent search in each language reaches the cited article.
5. **Code signs.** A receipt with SHA-256 fingerprints of model, text and quotes.

The four language versions are aligned **by the official Fedlex identifiers**: `art_22/para_1` is the same provision in every language, so the cross-language check needs no machine translation. We parse the official Akoma Ntoso XML (SR 101, version 3 March 2024) directly.

Stack: Apertus 1.5 8B (Q4_K_M GGUF) on llama.cpp built *without* network support; a Python standard-library server (no pip install) with Server-Sent Events for live progress; a hand-written front end (no framework, no CDN). The interface reproduces the design system of **America.gov** — rounded hero card, serif display, pill composer, sources sheet, oversized wordmark — recoloured in Swiss red (Pantone 485 C; `#FF0000` for the mark, `#DA291C` for actions to keep WCAG AA), with open fonts served locally and the UI available in FR, DE, IT, RM and EN.

### Measured, not promised

Same local model, same questions, with and without Belegt. 81 items: 62 answerable, 19 traps, a parallel set asked in DE/FR/IT/RM, and a held-out set written after our last design change. Temperature 0, 95% Wilson intervals.

| | Apertus alone | Apertus + Belegt |
|---|---|---|
| Cites a correct article | 26/62 = 42% [30–54] | **51/62 = 82% [71–90]** |
| Publishes a wrong or invented article | 48/81 = 59% [48–69] | **4/81 = 5% [2–12]** |
| Trap questions refused | 6/19 = 32% [15–54] | **19/19 = 100% [83–100]** |
| Same answer in all 4 languages | 4/10 = 40% [17–69] | **8/10 = 80% [49–94]** |
| Abstains although an answer exists | — | 9/62 = 15% [8–25] |

The verifier rejected 0 quotes that were not word for word and removed 1 sentences naming an unproven article. Median latency: 49.2 s per answer on 4 CPU cores. Every item and raw output is in `eval/`.

### Challenges we ran into

- **Lexical gaps.** Citizens say “demonstrate”, the Constitution says “freedom of assembly”. Letting Apertus rewrite the query in the Constitution’s vocabulary — but never answer at that stage — fixed most of it.
- **Paragraph vs article.** Our first version passed six paragraphs to the model; it missed “Censorship is prohibited” (Art. 17 para. 2) when para. 1 ranked first, and confused the President of the Confederation (Art. 176) with the presidents of the chambers (Art. 152). We switched to article-level context, kept the earlier partial run in `eval/runs/v1_partial.jsonl`, and added a held-out set written after the change.
- **What a verifier can and cannot prove.** Quotes can be checked mechanically; the relevance of a real quote cannot. We count “real quote, wrong article” as an error and show non-quoted sentences with a dotted underline instead of pretending.
- **CPU-only.** 8B at 4 bits on four cores means about a minute per answer. We show live progress with “AI / Code” labels so the wait is legible.

### Accomplishments we’re proud of

- A refusal that is useful: closest articles, and an explicit statement of what cannot be claimed.
- Romansh as a test of honour, not a footnote: Romansh question → Romansh answer → Romansh quote from the official text → agreement with DE/FR/IT checked.
- Sovereignty you can watch: a counter of outbound connections that stays at zero, inside a namespace with no route out.
- A receipt format small enough to read and strict enough to audit.

### What we learned

Apertus is good at understanding a question and rephrasing it in four languages, and good at choosing a relevant quote when the right article is in front of it. Alone, it is unreliable at article numbers. The productive split is: let the model do language, let code do truth.

### What’s next

- Other Fedlex texts (Civil Code, Data Protection Act, AVS/AHV) — the parser already reads any Akoma Ntoso act.
- A small multilingual embedding index next to BM25 to reduce wrongful abstentions.
- Native-speaker review of the Romansh questions and interface.
- Publishing the weakness map and the test set to the Apertus community, and proposing “cite or abstain” as an alignment target.

---

## For judges and organisers (Additional info — not public)

- **Run it in 10 minutes:** see README “Quick start”. Python ≥ 3.10, no pip dependencies; llama.cpp + the GGUF; `scripts/start.sh`.
- **Offline proof:** `sudo scripts/offline_demo.sh` starts llama.cpp and Belegt in a fresh network namespace (loopback only) and prints the routing table and a failed request to fedlex.admin.ch before serving.
- **Reproduce the numbers:** `python eval/run_eval.py && python eval/score.py` (≈ 75 s per item on 4 CPU cores). Baseline trap answers were labelled by hand in `eval/manual_labels.json` with a one-line justification each.
- **Honesty notes:** the verifier proves quotes exist, not that the paraphrase is right. Romansh questions were written by the team, not by native speakers. The design reproduces America.gov’s *structure*; no asset of that site is used, the Swiss coat of arms is not used, and the prototype is clearly labelled as unofficial.
- **File to upload:** `docs/submission/Belegt-submission.pdf` (or the zip `docs/submission/Belegt-submission.zip` with PDF + deck + video).
