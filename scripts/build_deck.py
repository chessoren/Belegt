"""Build the pitch deck (HTML, 1500x1000 per slide = 3:2) from the real evaluation numbers.

    python scripts/build_deck.py && node scripts/render_deck.mjs
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
S = json.loads((ROOT / "eval" / "summary.json").read_text())
M = S["metrics"]


def pct(k, who):
    v = M[k]
    return round(100 * v[who] / v["n"]) if v["n"] else 0


def ci(k, who):
    return M[k][f"{who}_fmt"].split("= ")[1]


def frac(k, who):
    return f"{M[k][who]}/{M[k]['n']}"


MARK = '<svg viewBox="0 0 18 18"><path d="M3.2 5.2 0.8 9l2.4 3.8M7.2 5.2 4.8 9l2.4 3.8M10.8 5.2 13.2 9l-2.4 3.8M14.8 5.2 17.2 9l-2.4 3.8" stroke="#fff" stroke-width="1.9" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
N = S["n_items"]
latency = S["latency_seconds"]["median"]
V = S["verifier"]
cost_per_1000 = round(latency * 1000 / 3600 * 0.15, 1)  # CHF, 4-vCPU VM at ~CHF 0.15/h (assumption)

slides = []


def foot(i):
    return f'<div class="foot"><b>Belegt<i>.</i></b><span>Hack Apertus 2026 · Track 2B · {i:02d}</span></div>'


def add(body, cls=""):
    i = len(slides) + 1
    slides.append(f'<section class="slide {cls}" id="s{i}">{body}{foot(i)}</section>')


# 1 — title
add(f"""
<div style="display:flex;justify-content:space-between;align-items:center"><span class="brand"><span class="mark">{MARK}</span><span class="serif" style="font-size:34px">Belegt</span></span><span class="kicker">Hack Apertus 2026 · Track 2B · Own Project</span></div>
<div style="flex:1;display:grid;grid-template-columns:1.25fr 1fr;gap:60px;align-items:center;margin-top:20px">
  <div><div class="serif" style="font-size:250px;line-height:.85;letter-spacing:-.06em">Belegt<span style="color:var(--color-swiss)">.</span></div>
  <div class="serif" style="font-size:54px;margin-top:34px;letter-spacing:-.03em">Cite, or stay silent.</div>
  <p class="lead" style="margin-top:18px">A Swiss-law assistant built on <b>Apertus</b> that answers only when it can prove every claim with the official text — in German, French, Italian and Romansh, fully offline.</p></div>
  <div class="shot" style="transform:rotate(1.5deg)"><img src="../img/answer_en.png" style="height:640px;object-fit:cover;object-position:top"></div>
</div>""")

# 2 — problem, with real outputs of Apertus alone
add(f"""
<span class="kicker">The problem</span>
<h2>A confident wrong answer cannot serve the state.</h2>
<div class="grid2" style="margin-top:40px">
  <div class="card line"><div class="muted" style="font-size:18px">Apertus 1.5 8B asked alone (in French): “Which article sets the maximum price of bread?” — real output</div>
    <p class="quote" style="margin:14px 0 0;color:var(--color-text-primary)">«L’<s>article 30</s> de la Constitution fédérale suisse fixe le prix maximum du pain. Ce prix ne doit pas dépasser le prix moyen du pain dans le canton…»</p>
    <p class="muted" style="margin:10px 0 0;font-size:18px;font-style:italic">“Article 30 of the Swiss Federal Constitution sets the maximum price of bread. This price must not exceed the average price of bread in the canton…”</p>
    <p style="margin-top:16px;font-size:20px"><span class="chip bad">✗ invented</span>&nbsp; No such provision. In DE/IT/RM: Art. 103, 31, 103.</p></div>
  <div class="card line"><div class="muted" style="font-size:18px">Same model (in French): “What are the national languages?” — real output</div>
    <p class="quote" style="margin:14px 0 0;color:var(--color-text-primary)">«Les langues nationales de la Suisse sont l’allemand, le français et l’italien.»</p>
    <p class="muted" style="margin:10px 0 0;font-size:18px;font-style:italic">“The national languages of Switzerland are German, French and Italian.”</p>
    <p style="margin-top:16px;font-size:20px"><span class="chip bad">✗ incomplete</span>&nbsp; Romansh is forgotten (Art. 4).</p></div>
</div>
<div class="grid3" style="margin-top:28px">
  <div class="card red"><div class="big" style="font-size:96px">{pct('wrong_article_published','baseline')}%</div><p>of Apertus-alone answers name a wrong or invented article ({frac('wrong_article_published','baseline')})</p></div>
  <div class="card"><h3>Inequality</h3><p>Four official languages: an answer that changes with the language is unequal treatment before the law.</p></div>
  <div class="card"><h3>Dependency</h3><p>Sending citizens’ questions to a foreign service is a sovereignty and data-protection problem first.</p></div>
</div>""")

# 3 — the rule
add("""
<span class="kicker">The idea</span>
<h2>One rule everyone understands: <span style="color:var(--color-red-600)">cite, or stay silent.</span></h2>
<p class="lead">Belegt asserts nothing it cannot point to in the official text. If the sentences don’t exist, the answer isn’t given.</p>
<div class="grid4" style="margin-top:64px">
  <div class="card"><div class="big" style="font-size:64px;color:var(--color-red-600)">01</div><h3 style="margin-top:22px">Proven</h3><p>Exact sentences of the law, highlighted, one click away.</p></div>
  <div class="card"><div class="big" style="font-size:64px;color:var(--color-red-600)">02</div><h3 style="margin-top:22px">Honest</h3><p>No evidence, no answer: it abstains, explains, and shows the closest articles.</p></div>
  <div class="card"><div class="big" style="font-size:64px;color:var(--color-red-600)">03</div><h3 style="margin-top:22px">One law, four languages</h3><p>DE · FR · IT · RM checked against each other; divergences are flagged.</p></div>
  <div class="card"><div class="big" style="font-size:64px;color:var(--color-red-600)">04</div><h3 style="margin-top:22px">A receipt</h3><p>Model hash, law version, evidence, checks, network state. Fileable.</p></div>
</div>""")

# 4 — who does what
add("""
<span class="kicker">How it works</span>
<h2>The AI understands and drafts. Plain code decides.</h2>
<div class="flow" style="margin-top:40px">
  <div class="step"><span class="chip ai">AI · Apertus</span><h4>Understand</h4><p>Rewrites the question in DE/FR/IT/RM with the Constitution’s own words (“demonstrate” → “freedom of assembly”).</p></div>
  <div class="step"><span class="chip code">Code</span><h4>Search</h4><p>BM25 on words + character 5-grams over 657 paragraphs × 4 languages; rank fusion; article-level context.</p></div>
  <div class="step"><span class="chip ai">AI · Apertus</span><h4>Draft</h4><p>1–3 sentences + quotes, JSON constrained by a grammar. May answer “nothing answers this”.</p></div>
  <div class="step v"><span class="chip code">Code · no AI</span><h4>Verify</h4><p>Deterministic rules below. Removes what is unproven. Abstains if nothing survives.</p></div>
  <div class="step"><span class="chip code">Code</span><h4>Receipt</h4><p>SHA-256 of model, law text and quotes; checks; network state; duration.</p></div>
</div>
<div class="rules">
  <div class="rule"><b>R1</b>The cited paragraph exists in the official text.</div>
  <div class="rule"><b>R2</b>The quote appears word for word.</div>
  <div class="rule"><b>R3</b>The quote is long enough to mean something.</div>
  <div class="rule"><b>R4</b>No article number in the answer that isn’t proven.</div>
  <div class="rule"><b>R5</b>No surviving evidence ⇒ abstain.</div>
  <div class="rule"><b>X</b>Independent search in each language reaches the same article.</div>
</div>
<p class="lead" style="font-size:21px;margin-top:26px">Languages are aligned by the official <b>Fedlex identifiers</b> (<code>art_22/para_1</code> is the same provision in every version): the cross-language check needs no machine translation.</p>""")

# 5 — scene 1
add("""
<div class="grid2" style="grid-template-columns:.8fr 1.2fr;gap:56px;flex:1;align-items:center">
  <div><span class="kicker">Scene 1 · the clear question</span><h2 style="font-size:56px">“Do I have the right to demonstrate in the street?”</h2>
  <p class="lead" style="font-size:23px">A short answer, and next to it the exact sentences of Art. 22, found word for word in the official text (English is not an official language, so quotes come from the official French version). One click opens the article in DE, FR, IT or RM.</p>
  <p class="lead" style="font-size:23px">In this run the German and Romansh searches did not reach Art. 22 on their own (“Straße” pulled road traffic, Art. 82): Belegt flags <b>2/4</b> instead of hiding it.</p>
  <p class="lead" style="font-size:23px">Sentences that rephrase instead of quoting are <span style="text-decoration:underline dotted;text-underline-offset:5px">dotted-underlined</span>.</p></div>
  <div class="shot"><img src="../img/answer_en.png" style="height:800px;object-fit:cover;object-position:top"></div>
</div>""")

# 6 — scene 2 romansh
add(f"""
<div class="grid2" style="grid-template-columns:1.2fr .8fr;gap:56px;flex:1;align-items:center">
  <div class="shot"><img src="../img/answer_rm.png" style="height:800px;object-fit:cover;object-position:0 18%"></div>
  <div><span class="kicker">Scene 2 · four languages, one law</span><h2 style="font-size:56px">The same question, in Romansh.</h2>
  <p class="lead" style="font-size:23px">Answer in Rumantsch, quotes from the official Romansh text, and proof that DE, FR, IT and RM lead to the same provision.</p>
  <div class="card" style="margin-top:26px"><div class="big" style="font-size:72px;color:var(--color-red-600)">{pct('lang_agree','belegt')}%</div><p>of questions asked in all four languages get the same answer with Belegt ({frac('lang_agree','belegt')}), vs {pct('lang_agree','baseline')}% for Apertus alone.</p></div></div>
</div>""")

# 7 — sovereignty
add(f"""
<span class="kicker">Sovereign, demonstrated</span>
<h2>Cable unplugged. Zero outbound connections.</h2>
<div class="grid2" style="grid-template-columns:1fr 1fr;gap:48px;margin-top:34px;align-items:start">
  <ul class="clean">
    <li><b>Apertus runs on the machine</b> — llama.cpp, CPU only, compiled without network support. Model file pinned by SHA-256.</li>
    <li><b>Belegt blocks and counts</b> every outbound connection and DNS lookup with a Python audit hook. The counter is in the UI and in every receipt.</li>
    <li><b>The demo runs in a Linux network namespace</b> with no interface but loopback: no route out exists at all (<code>scripts/offline_demo.sh</code>).</li>
    <li><b>No CDN, no tracker</b>: fonts and scripts are served by Belegt itself. Nothing is stored server-side.</li>
  </ul>
  <div class="shot"><img src="../img/network.png" style="height:520px;object-fit:cover;object-position:right top"></div>
</div>""")

# 8 — trap
add("""
<div class="grid2" style="grid-template-columns:.8fr 1.2fr;gap:56px;flex:1;align-items:center">
  <div><span class="kicker">Scene 3 · the trap</span><h2 style="font-size:56px">“Which article sets the maximum price of bread?”</h2>
  <p class="lead" style="font-size:23px">None does. Belegt says so, points to the closest articles for the reader to check (food security, competition policy), and claims nothing.</p>
  <p class="lead" style="font-size:23px">Abstention is the expected behaviour, measured and shown — not hidden.</p></div>
  <div class="shot"><img src="../img/refusal.png" style="height:700px;object-fit:cover;object-position:top"></div>
</div>""")

# 9 — receipt
add("""
<div class="grid2" style="grid-template-columns:1.1fr .9fr;gap:56px;flex:1;align-items:center">
  <div class="shot"><img src="../img/receipt.png" style="height:760px;object-fit:cover;object-position:right top"></div>
  <div><span class="kicker">Scene 4 · the auditor</span><h2 style="font-size:56px">A receipt for every answer.</h2>
  <ul class="clean" style="margin-top:28px">
    <li><b>Model</b> name, runtime, temperature, seed, SHA-256 of the weights</li>
    <li><b>Law</b> SR 101, version 03.03.2024, SHA-256 of the text</li>
    <li><b>Evidence</b> each quote with its hash and character span</li>
    <li><b>Checks</b> R1–R5 and cross-language agreement</li>
    <li><b>Network</b> offline state and outbound-connection count</li></ul>
  <p class="lead" style="font-size:21px">Downloadable as JSON, printable. It turns a demo into an infrastructure component.</p></div>
</div>""")

# 10 — numbers
rows = [
    ("Cites a correct article (answerable)", "correct_article"),
    ("Publishes a wrong or invented article", "wrong_article_published"),
    ("Trap questions refused", "trap_refused"),
    ("Same answer in all 4 languages", "lang_agree"),
    ("Correct article — Romansh questions", "correct_rm"),
]
trs = "".join(f"<tr><td>{l}</td><td class='n'>{pct(k,'baseline')}% <span class='ci'>{ci(k,'baseline')}</span></td><td class='n'><b>{pct(k,'belegt')}%</b> <span class='ci'>{ci(k,'belegt')}</span></td></tr>" for l, k in rows if k in M)
add(f"""
<span class="kicker">Measured, not promised</span>
<h2>Same model. Same questions. With and without Belegt.</h2>
<div class="grid2" style="grid-template-columns:1.25fr .75fr;gap:48px;margin-top:30px;align-items:start">
  <div><table><thead><tr><th></th><th style="text-align:right">Apertus alone</th><th style="text-align:right">Apertus + Belegt</th></tr></thead><tbody>{trs}
  <tr><td>Abstains although an answer exists</td><td class='n'>—</td><td class='n'><b>{pct('over_refusal','belegt')}%</b> <span class='ci'>{ci('over_refusal','belegt')}</span></td></tr></tbody></table>
  <p class="muted" style="font-size:17px;margin-top:16px">{N} items: {S['answerable']} answerable, {S['traps']} traps; parallel set asked in DE/FR/IT/RM; held-out questions written after the last design change. Apertus 1.5 8B Q4_K_M, local, temperature 0. 95% Wilson intervals. Baseline trap answers labelled by hand, with justification. Raw outputs: <code>eval/</code>.</p></div>
  <div class="card ink"><h3>What the verifier caught</h3><p style="font-size:21px;line-height:1.6">{V['quotes_rejected']} quotes not found word for word<br>{V['sentences_removed']} sentence(s) naming an unproven article<br>{V['model_said_answerable_but_abstained']} drafts with no surviving evidence<br><br>Median latency {latency} s per answer on 4 CPU cores.</p></div>
</div>""")

# 11 — criteria
add(f"""
<span class="kicker">Track 2B criteria</span>
<h2>Built against the five published criteria.</h2>
<table style="margin-top:44px;font-size:22px"><thead><tr><th style="width:24%">Criterion</th><th>How Belegt answers</th><th style="width:27%">Proof to check</th></tr></thead><tbody>
<tr><td><b>Meaningful use of AI</b></td><td>Apertus understands, rewrites in four languages and drafts. Verification is deterministic.</td><td>“AI / Code” chips on every step; trap refusal</td></tr>
<tr><td><b>Technical rigour</b></td><td>Baseline vs Belegt on the same model, Wilson intervals, held-out set, failures kept visible.</td><td><code>eval/results.md</code>, raw runs</td></tr>
<tr><td><b>Value, cost, scale</b></td><td>8B model, 4-bit, CPU. ≈ CHF {cost_per_1000} per 1,000 answers on a 4-vCPU VM (assumption: CHF 0.15/h).</td><td>Latency in every receipt</td></tr>
<tr><td><b>Sovereign deployability</b></td><td>Offline, local weights, no external service, outbound audit, receipts.</td><td><code>offline_demo.sh</code> + network panel</td></tr>
<tr><td><b>Implementation feasibility</b></td><td>Deliberately small scope that fully works; Python stdlib + llama.cpp; one command to run.</td><td>Jury can run it in 10 minutes</td></tr>
</tbody></table>""")

# 12 — value & next
add("""
<span class="kicker">Who it is for</span>
<h2>A blueprint others can take tomorrow.</h2>
<div class="grid3" style="margin-top:56px">
  <div class="card" style="min-height:300px"><h3>Citizens & schools</h3><p>Understand rights with the source one click away; teach critical thinking about AI with an AI that shows its evidence.</p></div>
  <div class="card" style="min-height:300px"><h3>Administrations</h3><p>Communes, cantons, Confederation: deployable without invented content or foreign dependency; receipts for the file.</p></div>
  <div class="card" style="min-height:300px"><h3>Regulated firms</h3><p>Banks, insurers, health: the same rule on their own texts — compliance needs traceability, not eloquence.</p></div>
</div>
<div class="card line" style="margin-top:28px;padding:40px"><h3>Next corpora (the method is the product)</h3><p>Civil Code (SR 210) · Data Protection Act (SR 235.1) · AVS/AHV (SR 831.10) · municipal regulations. Any Akoma Ntoso text from Fedlex drops in: <code>belegt/corpus.py</code> parses the official XML and keeps the official IDs.</p></div>""")

# 13 — giving back + limits
add("""
<span class="kicker">What Belegt gives back to Apertus</span>
<h2>A contribution, not just a demo.</h2>
<div class="grid2" style="margin-top:60px;gap:48px;flex:1;align-items:start">
  <ul class="clean">
    <li><b>A weakness map</b>: where Apertus cites correctly, invents, or diverges across languages — with examples.</li>
    <li><b>A reusable test set</b>: questions, traps, the same questions in DE/FR/IT/RM, gold articles.</li>
    <li><b>A behaviour worth training</b>: cite or abstain, as a target for future alignment work.</li>
    <li><b>A receipt format</b> other projects can adopt. Everything Apache-2.0.</li>
  </ul>
  <div class="card ink" style="padding:44px"><h3>Limits, said first</h3><p style="font-size:23px;line-height:1.6;margin-top:14px">Not legal advice. The verifier proves quotes exist — not that the paraphrase is right, nor that the quoted article is the relevant one (those cases are counted as errors). Lexical search can miss the article → abstention. ≈ 50 s per answer on 4 CPU cores. Romansh test questions written by the team, not native speakers. CPU inference is not bit-for-bit reproducible: one demo take refused the Romansh question (wrongful abstention, never an invention).</p></div>
</div>""")

# 14 — close
add(f"""
<div style="flex:1;display:flex;flex-direction:column;justify-content:center">
  <div class="serif" style="font-size:76px;line-height:1.05;max-width:1250px;letter-spacing:-.035em">“Apertus was built open so that trust could be verified. Belegt is a first public demonstration.”</div>
  <div class="grid3" style="margin-top:60px">
    <div><div class="kicker">Run it</div><p class="lead" style="font-size:22px;margin-top:8px"><code>scripts/start.sh</code><br><code>sudo scripts/offline_demo.sh</code></p></div>
    <div><div class="kicker">Code & data</div><p class="lead" style="font-size:22px;margin-top:8px">github.com/chessoren/Belegt<br>Apache-2.0</p></div>
    <div><div class="kicker">Built with</div><p class="lead" style="font-size:22px;margin-top:8px">Apertus 1.5 8B · llama.cpp · Fedlex · Python stdlib</p></div>
  </div>
  <div class="serif" style="font-size:44px;margin-top:70px">Prove it, or stay silent.</div>
</div>""")

html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Belegt — deck</title>
<link rel="stylesheet" href="deck.css"></head><body>{''.join(slides)}</body></html>"""
(ROOT / "docs" / "deck" / "deck.html").write_text(html)
print(len(slides), "slides")
