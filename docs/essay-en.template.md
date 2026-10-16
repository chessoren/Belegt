# Belegt — prove it, or stay silent

*Project essay · Hack Apertus 2026 · Track 2B “Own Project” · @Oren*

## A confidently wrong AI cannot serve the state

We started with a simple experiment. We asked Apertus, the open Swiss model, ordinary citizens’ questions about the Federal Constitution and asked it to name the relevant article. “Which article of the Constitution sets the maximum price of bread?” — *“Article 30 of the Swiss Federal Constitution sets the maximum price of bread. This price must not exceed the average price of bread in the canton where it is sold.”* No such provision exists. Asked the same question in German, Italian and Romansh, it invented three other articles (103, 31, 103). “What are the national languages?” — *“German, French and Italian.”* Romansh had disappeared.

This is not a flaw specific to Apertus: every large language model writes with the same fluency whether it is right or wrong. On our test set, Apertus asked alone named a wrong or invented article in **{{WRONG_BASE}}%** of its answers. For a consumer chatbot that is annoying. For a public administration it is disqualifying: a citizen cannot guess that a plausible article number is false, and a disclaimer such as “please verify” only shifts the burden onto them.

The brake on AI in the public sector is therefore neither power nor price. It is trust. And trust cannot be decreed: it has to be verifiable.

## A rule everyone understands

Belegt — German for *substantiated, documented* — rests on a single rule: **cite, or stay silent**. Belegt asserts nothing it cannot point to in the official text. Every answer comes with the exact sentences of the Constitution it rests on, highlighted in the article, one click away. If those sentences don’t exist, the answer is not given: Belegt says so, explains why, and lists the closest articles for the reader to check — without claiming anything.

“Which article of the Constitution sets the maximum price of bread?” None. An ordinary assistant would invent a plausible article. Belegt answers: *no proof, no answer*, and suggests reading the articles on food security and competition policy.

## Who does what

The heart of the project is a clear division of roles. The AI does what it is good at: understanding a question written by a human and rephrasing it. Apertus turns “demonstrate in the street” into “freedom of assembly” in German, French, Italian and Romansh, using the Constitution’s own vocabulary. It then drafts a short answer and picks its quotes among the retrieved articles.

Verification is not left to the AI. Simple, deterministic code applies five rules: the cited paragraph exists; the quote appears in it word for word; the quote is long enough to carry meaning; no unproven article number appears in the answer (otherwise the sentence is removed); and if no evidence survives, Belegt abstains. A sixth check verifies that a search run independently in each of the four languages reaches the same article.

The split is visible on screen: every step carries an “AI” or a “Code” label. Users can see what is probabilistic and what is not.

## Four languages, one law

In Switzerland, equality between languages is not a nice-to-have: it is a constitutional requirement. A tool that answers differently depending on the language of the question creates inequality before the law. Belegt treats the four official versions on an equal footing, Romansh included.

We found an elegant way to do it: the texts published by Fedlex carry official identifiers that are identical in every language. Paragraph `art_22/para_1` is the same provision in German, French, Italian and Romansh, so the cross-language check needs no machine translation. Ask in Romansh: the answer comes in Romansh, the quote comes from the official Romansh text, and a panel shows the same provision in the three other languages. If a version diverged, a banner would say so instead of silently choosing. With Belegt, questions asked in all four languages received the same answer in **{{LANG_BELEGT}}%** of cases, against **{{LANG_BASE}}%** for Apertus alone.

English questions are welcome too: since English is not an official language of the Confederation, Belegt answers in English and quotes the official French text.

## Sovereignty, demonstrated rather than claimed

Everyone says “sovereign”. We wanted to show it. Apertus runs on the machine, with llama.cpp built without network support; the model file is identified by its SHA-256 fingerprint. The Belegt server installs an audit hook that blocks and counts every outbound connection or DNS lookup; the counter is always visible and written into every receipt. Finally, the demo runs inside an isolated Linux network namespace that has no interface except loopback: there is simply no route out. The counter stays at zero, and the answers still arrive.

## A receipt for every answer

Every answer produces a readable receipt: which model answered (and its fingerprint), which version of the law was used (and its fingerprint), which evidence was found (each quote with its hash and exact position in the text), which checks passed, and what state the network was in. A legal team or an auditor can download it and file it as supporting evidence. That is what turns a demo into a piece of infrastructure.

## Measured, not promised

We don’t say “it works well”. We compared the same local model, on the same questions, with and without Belegt: {{N}} questions, including {{N_TRAP}} traps, a set asked in all four languages, and a held-out set written after our last design change.

| | Apertus alone | Apertus + Belegt |
|---|---|---|
| Cites a correct article | {{CORRECT_BASE_F}} | **{{CORRECT_BELEGT_F}}** |
| Publishes a wrong or invented article | {{WRONG_BASE_F}} | **{{WRONG_BELEGT_F}}** |
| Trap questions refused | {{TRAP_BASE_F}} | **{{TRAP_BELEGT_F}}** |
| Same answer in all 4 languages | {{LANG_BASE_F}} | **{{LANG_BELEGT_F}}** |
| Abstains although an answer exists | — | {{OVER_BELEGT_F}} |

*95% confidence intervals (Wilson). All raw outputs are published in the repository.*

These numbers come at a price we accept: Belegt sometimes abstains when an answer existed, because lexical search missed the right article. We prefer one silence too many to one invention.

## What Belegt is not, and its limits

Belegt is not a legal adviser: it helps people find and read the official text, not decide an individual case. The verifier guarantees that quotes exist word for word; it does not guarantee that the paraphrase around them is right, nor that the quoted article is the most relevant one. That is why sentences that are not quotes are dotted-underlined, and why a “real quote from the wrong article” counts as an error in our measurements. The model runs at 4 bits on a CPU: an answer takes about 50 seconds (measured median). Our Romansh test questions were written by the team, not by native speakers. And local CPU inference is not bit-for-bit reproducible: in one of our demo recording takes the Romansh question was refused — a wrongful abstention, never an invention.

## What Belegt gives back to Apertus

A project that takes from a model without giving anything back is a demo; a project that gives knowledge back is a contribution. Belegt publishes a map of Apertus’s weaknesses (where it cites correctly, where it invents, where it diverges from one language to another), a reusable question set with its traps and its four-language versions, a behaviour worth aiming for in future alignment work — cite or abstain — and a receipt format other projects can adopt. Everything is released under the Apache-2.0 licence.

The Constitution is only a test bed. The method applies to any official text published by Fedlex: the Civil Code, the Data Protection Act, old-age insurance, and tomorrow the municipal regulations a small business or a school has to follow.

*Apertus was built open so that trust could be verified. Belegt is a first public demonstration.*

**Prove it, or stay silent.**
