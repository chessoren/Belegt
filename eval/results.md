# Belegt — evaluation results

Run file: `eval/runs/run.jsonl` · 12 items (12 answerable, 0 traps) · model: Apertus 1.5 8B Q4_K_M, local llama.cpp on 4 CPU cores, temperature 0.

Both systems use **the same local model**. *Baseline* = Apertus asked directly (asked to name the article). *Belegt* = Apertus + retrieval + deterministic verifier. 95% Wilson intervals in brackets.

| Metric | Apertus alone | Apertus + Belegt |
|---|---|---|
| Cites a correct article (answerable questions) | 4/12 = 33% [14–61] | **11/12 = 92% [65–99]** |
| Publishes a wrong or invented article (all items) | 8/12 = 67% [39–86] | **2/12 = 17% [5–45]** |
| Publishes a wrong article (answerable questions) | 8/12 = 67% [39–86] | **2/12 = 17% [5–45]** |
| Abstains although an answer exists | n/a (never abstains) | **0/12 = 0% [0–24]** |
| Trap questions refused | 0/0 = 0% [0–0] | **0/0 = 0% [0–0]** |
| Trap questions answered with an article | 0/0 = 0% [0–0] | **0/0 = 0% [0–0]** |
| Correct article — French | 4/12 = 33% [14–61] | **11/12 = 92% [65–99]** |
| Same answer in all 4 languages (parallel groups) | 0/0 = 0% [0–0] | **0/0 = 0% [0–0]** |

## What the verifier caught

- Quotes rejected because they were not found word for word: **0** (in 0 answers).
- Sentences removed because they named an unproven article: **0**.
- Answers where the model said 'answerable' but no evidence survived (Belegt abstained): **0**.
- Ablation, retrieval *without* verifier: raw drafts that name a wrong article: **1**.

Latency per answer (CPU, 4 cores): median 67.4 s, p90 81.3 s.

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

Raw outputs (questions, drafts, quotes, rejected quotes, baseline answers) are in the run file.
