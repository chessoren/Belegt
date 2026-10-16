# Belegt — evaluation results

Run file: `eval/runs/run.jsonl` · 81 items (62 answerable, 19 traps) · model: Apertus 1.5 8B Q4_K_M, local llama.cpp on 4 CPU cores, temperature 0.

Both systems use **the same local model**. *Baseline* = Apertus asked directly (asked to name the article). *Belegt* = Apertus + retrieval + deterministic verifier. 95% Wilson intervals in brackets.

| Metric | Apertus alone | Apertus + Belegt |
|---|---|---|
| Cites a correct article (answerable questions) | 26/62 = 42% [30–54] | **51/62 = 82% [71–90]** |
| Publishes a wrong or invented article (all items) | 48/81 = 59% [48–69] | **4/81 = 5% [2–12]** |
| Publishes a wrong article (answerable questions) | 35/62 = 56% [44–68] | **4/62 = 6% [3–15]** |
| Abstains although an answer exists | n/a (never abstains) | **9/62 = 15% [8–25]** |
| Trap questions refused | 6/19 = 32% [15–54] | **19/19 = 100% [83–100]** |
| Trap questions answered with an article | 13/19 = 68% [46–85] | **0/19 = 0% [0–17]** |
| Correct article — French | 16/33 = 48% [33–65] | **25/33 = 76% [59–87]** |
| Correct article — German | 3/10 = 30% [11–60] | **8/10 = 80% [49–94]** |
| Correct article — Italian | 4/10 = 40% [17–69] | **10/10 = 100% [72–100]** |
| Correct article — Romansh | 3/9 = 33% [12–65] | **8/9 = 89% [56–98]** |
| Same answer in all 4 languages (parallel groups) | 4/10 = 40% [17–69] | **8/10 = 80% [49–94]** |

## What the verifier caught

- Quotes rejected because they were not found word for word: **0** (in 0 answers).
- Sentences removed because they named an unproven article: **1**.
- Answers where the model said 'answerable' but no evidence survived (Belegt abstained): **0**.
- Ablation, retrieval *without* verifier: raw drafts that name a wrong article: **1**.

## Held-out questions (written after the last design change)

- Answerable: correct article Apertus alone 3/8 = 38% [14–69] · Belegt 5/8 = 62% [31–86]
- Traps refused: Apertus alone 2/3 = 67% [21–94] · Belegt 3/3 = 100% [44–100]

## Weakness map (every Belegt failure, kept visible)

- **q08** (fr) real quote, wrong article — cited 140, gold art_141 — Combien de signatures faut-il pour demander un référendum contre une loi fédérale ?
- **q11** (fr) real quote, wrong article — cited 152, 176, gold art_176 — Pour combien de temps le président de la Confédération est-il élu ?
- **q18** (fr) wrongful abstention — gold art_25; closest shown: Art. 53, Art. 52, Art. 159 — Un citoyen suisse peut-il être livré à un pays étranger sans son accord ?
- **q19** (fr) wrongful abstention — gold art_14; closest shown: Art. 121a, Art. 73, Art. 127 — Le droit au mariage est-il garanti ?
- **q25** (fr) wrongful abstention — gold art_80; closest shown: Art. 61, Art. 121 — Qui légifère sur la protection des animaux ?
- **q27** (fr) wrongful abstention — gold art_106; closest shown: Art. 188, Art. 122, Art. 191a — Qui autorise l'ouverture d'un casino ?
- **q28** (fr) wrongful abstention — gold art_5; closest shown: Art. 3, Art. 2, Art. 129a — L'activité de l'État doit-elle respecter le droit international ?
- **q30** (fr) wrongful abstention — gold art_148; closest shown: Art. 163, Art. 175, Art. 154 — De quelles chambres se compose l'Assemblée fédérale ?
- **q02-it** (it) real quote, wrong article — cited 4, 70, gold art_4 — Quali sono le lingue nazionali della Svizzera?
- **q09-de** (de) wrongful abstention — gold art_175; closest shown: Art. 176, Art. 151, Art. 144 — Aus wie vielen Mitgliedern besteht der Bundesrat?
- **h05** (de) wrongful abstention — gold art_175; closest shown: Art. 136, Art. 34, Art. 39 — Wer wählt die Mitglieder des Bundesrates?
- **h06** (rm) wrongful abstention — gold art_24; closest shown: Art. 21, Art. 18, Art. 23 — Han las Svizras ed ils Svizzers il dretg da bandunar la Svizra?
- **h07** (fr) real quote, wrong article — cited 196, gold art_128 — La Confédération peut-elle percevoir un impôt fédéral direct ?

Scoring is conservative: a real quote from a neighbouring article counts as an error even when it is defensible (e.g. Art. 70 *official languages* cited next to Art. 4, or the transitional provision of Art. 196 on the direct federal tax).

Latency per answer (CPU, 4 cores): median 49.2 s, p90 71.4 s.

## Every item

| id | lang | gold | Belegt | Belegt articles | baseline articles | baseline trap label |
|---|---|---|---|---|---|---|
| q01 | fr | 22 | answered | 22 | 16 |  |
| q02 | fr | 4 | answered | 4 | 4 |  |
| q03 | fr | 136 | answered | 136 | 136 |  |
| q04 | fr | 10 | answered | 10 | 10 |  |
| q05 | fr | 59 | answered | 59 | 12 |  |
| q06 | fr | 8 | answered | 8 | 8 |  |
| q07 | fr | 139 | answered | 139 | 100 |  |
| q08 | fr | 141 | answered | 140 | 140 |  |
| q09 | fr | 175 | answered | 175 | 132 |  |
| q10 | fr | 149 | answered | 149 | 146 |  |
| q11 | fr | 176 | answered | 152, 176 | 124 |  |
| q12 | fr | 17 | answered | 17 | 16 |  |
| q13 | fr | 19, 62 | answered | 62 | 62 |  |
| q14 | fr | 12 | answered | 12 | 12 |  |
| q15 | fr | 15 | answered | 15 | 15 |  |
| q16 | fr | 24 | answered | 24 | 12 |  |
| q17 | fr | 10, 25 | answered | 10 | 10 |  |
| q18 | fr | 25 | abstained | — | 13 |  |
| q19 | fr | 14 | abstained | — | 14 |  |
| q20 | fr | 26 | answered | 26 | 61 |  |
| q21 | fr | 28 | answered | 28 | 28 |  |
| q22 | fr | 3 | answered | 3 | 3 |  |
| q23 | fr | 149 | answered | 149 | 144 |  |
| q24 | fr | 13 | answered | 13 | 13 |  |
| q25 | fr | 80 | abstained | — | 80 |  |
| q26 | fr | 33 | answered | 33 | 103 |  |
| q27 | fr | 106 | abstained | — | 106 |  |
| q28 | fr | 5 | abstained | — | 53 |  |
| q29 | fr | 29 | answered | 29 | 29 |  |
| q30 | fr | 148 | abstained | — | 144 |  |
| t01 | fr | — | abstained | — | 30 | invented |
| t02 | fr | — | abstained | — | 36 | invented |
| t03 | fr | — | abstained | — | 3 | invented |
| t04 | fr | — | abstained | — | 30 | invented |
| t05 | fr | — | abstained | — | 117 | invented |
| t06 | fr | — | abstained | — | 4 | refused |
| t07 | fr | — | abstained | — | — | refused |
| t08 | fr | — | abstained | — | 2 | refused |
| t09 | fr | — | abstained | — | — | refused |
| t10 | fr | — | abstained | — | 134 | invented |
| q01-de | de | 22 | answered | 22 | 16 |  |
| q01-it | it | 22 | answered | 22 | 16 |  |
| q01-rm | rm | 22 | answered | 22 | 16 |  |
| q02-de | de | 4 | answered | 4 | — |  |
| q02-it | it | 4 | answered | 4, 70 | 4 |  |
| q02-rm | rm | 4 | answered | 4 | 4 |  |
| q03-de | de | 136 | answered | 136 | 134 |  |
| q03-it | it | 136 | answered | 136 | 34 |  |
| q03-rm | rm | 136 | answered | 136 | 133 |  |
| q04-de | de | 10 | answered | 10 | 10 |  |
| q04-it | it | 10 | answered | 10 | 10 |  |
| q04-rm | rm | 10 | answered | 10 | 10 |  |
| q07-de | de | 139 | answered | 139 | 114 |  |
| q07-it | it | 139 | answered | 139 | 100 |  |
| q07-rm | rm | 139 | answered | 139 | 114 |  |
| q09-de | de | 175 | abstained | — | 104 |  |
| q09-it | it | 175 | answered | 175 | 104 |  |
| q09-rm | rm | 175 | answered | 175 | 102 |  |
| q12-de | de | 17 | answered | 17 | 16 |  |
| q12-it | it | 17 | answered | 17 | 16 |  |
| q12-rm | rm | 17 | answered | 17 | 16 |  |
| q15-de | de | 15 | answered | 15 | 15 |  |
| q15-it | it | 15 | answered | 15 | 15 |  |
| q15-rm | rm | 15 | answered | 15 | 15 |  |
| t01-de | de | — | abstained | — | 103 | invented |
| t01-it | it | — | abstained | — | 31 | invented |
| t01-rm | rm | — | abstained | — | 103 | invented |
| t10-de | de | — | abstained | — | 114 | invented |
| t10-it | it | — | abstained | — | 26 | invented |
| t10-rm | rm | — | abstained | — | 13 | invented |
| h01 | fr | 27 | answered | 27 | 27 |  |
| h02 | de | 19, 62 | answered | 19 | 62 |  |
| h03 | it | 82 | answered | 82 | 86 |  |
| h04 | fr | 56 | answered | 56 | 54 |  |
| h05 | de | 175 | abstained | — | 124 |  |
| h06 | rm | 24 | abstained | — | 36 |  |
| h07 | fr | 128 | answered | 196 | 121 |  |
| h08 | it | 13 | answered | 13 | 13 |  |
| h09 | fr | — | abstained | — | 32 | invented |
| h10 | de | — | abstained | — | 1 | refused |
| h11 | it | — | abstained | — | — | refused |

Raw outputs (questions, drafts, quotes, rejected quotes, baseline answers) are in the run file.
