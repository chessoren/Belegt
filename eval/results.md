# Belegt — evaluation results

Run file: `eval/runs/run.jsonl` · 10 items (10 answerable, 0 traps) · model: Apertus 1.5 8B Q4_K_M, local llama.cpp on 4 CPU cores, temperature 0.

Both systems use **the same local model**. *Baseline* = Apertus asked directly (asked to name the article). *Belegt* = Apertus + retrieval + deterministic verifier. 95% Wilson intervals in brackets.

| Metric | Apertus alone | Apertus + Belegt |
|---|---|---|
| Cites a correct article (answerable questions) | 4/10 = 40% [17–69] | **10/10 = 100% [72–100]** |
| Publishes a wrong or invented article (all items) | 6/10 = 60% [31–83] | **0/10 = 0% [0–28]** |
| Publishes a wrong article (answerable questions) | 6/10 = 60% [31–83] | **0/10 = 0% [0–28]** |
| Abstains although an answer exists | n/a (never abstains) | **0/10 = 0% [0–28]** |
| Trap questions refused | 0/0 = 0% [0–0] | **0/0 = 0% [0–0]** |
| Trap questions answered with an article | 0/0 = 0% [0–0] | **0/0 = 0% [0–0]** |
| Correct article — French | 4/10 = 40% [17–69] | **10/10 = 100% [72–100]** |
| Same answer in all 4 languages (parallel groups) | 0/0 = 0% [0–0] | **0/0 = 0% [0–0]** |

## What the verifier caught

- Quotes rejected because they were not found word for word: **1** (in 1 answers).
- Sentences removed because they named an unproven article: **1**.
- Answers where the model said 'answerable' but no evidence survived (Belegt abstained): **0**.
- Ablation, retrieval *without* verifier: raw drafts that name a wrong article: **1**.

Latency per answer (CPU, 4 cores): median 61.9 s, p90 87.9 s.

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
| q08 | fr | 141 | answered | 141 | 140 |  |
| q09 | fr | 175 | answered | 175 | 134 |  |
| q10 | fr | 149 | answered | 149 | 146 |  |

Raw outputs (questions, drafts, quotes, rejected quotes, baseline answers) are in the run file.
