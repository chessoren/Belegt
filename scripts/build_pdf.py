"""Build the submission PDF (A4) from docs/devpost.md + docs/essai-fr.md + screenshots.

    python scripts/build_pdf.py && node scripts/render_pdf.mjs
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
S = json.loads((ROOT / "eval" / "summary.json").read_text())


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<i>\1</i>", s)
    s = re.sub(r"(https?://[^\s<)]+)", r'<a href="\1">\1</a>', s)
    return s


def md(text):
    out, lines, i = [], text.splitlines(), 0
    while i < len(lines):
        l = lines[i]
        if not l.strip() or l.strip() == "---":
            i += 1; continue
        if l.startswith("#"):
            n = len(l) - len(l.lstrip("#"))
            out.append(f"<h{n}>{inline(l[n:].strip())}</h{n}>"); i += 1; continue
        if l.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i][1:].strip()); i += 1
            out.append(f"<blockquote>{inline(' '.join(buf))}</blockquote>"); continue
        if l.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                if not re.match(r"^\|[\s\-|:]+\|$", lines[i]):
                    rows.append([c.strip() for c in lines[i].strip("|").split("|")])
                i += 1
            t = "<table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in rows[0]) + "</tr></thead><tbody>"
            t += "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows[1:]) + "</tbody></table>"
            out.append(t); continue
        if re.match(r"^\s*[-*] ", l):
            items = []
            while i < len(lines) and re.match(r"^\s*[-*] ", lines[i]):
                items.append(re.sub(r"^\s*[-*] ", "", lines[i])); i += 1
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>"); continue
        if re.match(r"^\d+\. ", l):
            items = []
            while i < len(lines) and re.match(r"^\d+\. ", lines[i]):
                items.append(re.sub(r"^\d+\. ", "", lines[i])); i += 1
            out.append("<ol>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ol>"); continue
        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#|\||>|\s*[-*] |\d+\. )", lines[i]):
            buf.append(lines[i].strip()); i += 1
        out.append(f"<p>{inline(' '.join(buf))}</p>")
    return "\n".join(out)


dev = (ROOT / "docs" / "devpost.md").read_text()
story = dev.split("## About the project (Devpost story — Markdown)")[1].split("## For judges and organisers")[0]
judges = dev.split("## For judges and organisers (Additional info — not public)")[1]
essai = (ROOT / "docs" / "essay-en.md").read_text()
tagline = re.search(r"## Tagline.*?\n\n\*\*(.+?)\*\*", dev, re.S).group(1)
tags = re.search(r"## 25 tags.*?\n\n(.+?)\n", dev, re.S).group(1)
M = S["metrics"]
pct = lambda k, w: round(100 * M[k][w] / M[k]["n"]) if M[k]["n"] else 0  # noqa: E731

doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Belegt — submission</title>
<style>
@font-face {{ font-family: Newsreader; src: url(../../web/fonts/newsreader-latin-standard-normal.woff2); font-weight: 200 800; }}
@font-face {{ font-family: Newsreader; src: url(../../web/fonts/newsreader-latin-standard-italic.woff2); font-weight: 200 800; font-style: italic; }}
@font-face {{ font-family: Inter; src: url(../../web/fonts/inter-latin-wght-normal.woff2); font-weight: 100 900; }}
@page {{ size: A4; margin: 18mm 18mm 20mm; }}
body {{ font-family: Inter, sans-serif; color: #1c0204; font-size: 10.2pt; line-height: 1.55; letter-spacing: -.01em; }}
h1, h2, h3 {{ font-family: Newsreader, serif; font-weight: 400; letter-spacing: -.025em; line-height: 1.1; }}
h1 {{ font-size: 30pt; margin: 0 0 8pt; }} h2 {{ font-size: 20pt; margin: 22pt 0 6pt; }} h3 {{ font-size: 14.5pt; margin: 16pt 0 4pt; }}
p, li {{ color: #1c0204d0; }} a {{ color: #c8102e; text-decoration: none; }}
code {{ font-family: ui-monospace, Menlo, monospace; font-size: 8.8pt; background: #8e0d140d; padding: 0 3px; border-radius: 3px; }}
table {{ width: 100%; border-collapse: collapse; margin: 8pt 0; font-size: 9.4pt; }} th, td {{ text-align: left; padding: 5pt 6pt; border-bottom: .6pt solid #1c02041f; vertical-align: top; }}
th {{ font-size: 8pt; text-transform: uppercase; letter-spacing: .05em; color: #1c020480; }}
blockquote {{ margin: 8pt 0; padding: 6pt 10pt; border-left: 2pt solid #da291c; background: #fdf3f2; }}
.cover {{ height: 252mm; overflow: hidden; display: flex; flex-direction: column; justify-content: space-between; page-break-after: always; }}
.mark {{ width: 34pt; height: 34pt; border-radius: 8pt; background: #ff0000; display: inline-grid; place-items: center; vertical-align: middle; }}
.big {{ font-family: Newsreader, serif; font-size: 96pt; line-height: .85; letter-spacing: -.06em; }}
.kicker {{ font-size: 8.5pt; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: #da291c; }}
.kpis {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10pt; }}
.kpi {{ border-radius: 12pt; background: #f7f7f7; padding: 12pt 14pt; }} .kpi.r {{ background: #da291c; color: #fff; }} .kpi.r p {{ color: #ffffffd0; }}
.kpi b {{ display: block; font-size: 26pt; letter-spacing: -.04em; line-height: 1; }} .kpi p {{ margin: 5pt 0 0; font-size: 8.8pt; line-height: 1.35; }}
.shots {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10pt; margin: 10pt 0; }} .shots img {{ width: 100%; border-radius: 8pt; border: .6pt solid #1c02041f; }}
.pb {{ page-break-before: always; }} .muted {{ color: #1c020490; font-size: 8.8pt; }}
</style></head><body>
<section class="cover">
  <div><span class="mark"><svg viewBox="0 0 18 18" width="24" height="24"><path d="M3.2 5.2 0.8 9l2.4 3.8M7.2 5.2 4.8 9l2.4 3.8M10.8 5.2 13.2 9l-2.4 3.8M14.8 5.2 17.2 9l-2.4 3.8" stroke="#fff" stroke-width="1.9" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
   <span class="kicker" style="margin-left:10pt">Hack Apertus 2026 · Track 2B · Own Project · submission</span></div>
  <div><div class="big">Belegt<span style="color:#ff0000">.</span></div>
   <p style="font-family:Newsreader,serif;font-size:24pt;color:#1c0204;margin:16pt 0 8pt;letter-spacing:-.02em">Cite, or stay silent.</p>
   <p style="font-size:12pt;max-width:150mm">{inline(tagline)}</p></div>
  <div class="kpis">
   <div class="kpi r"><b>{pct('wrong_article_published','baseline')}% → {pct('wrong_article_published','belegt')}%</b><p>answers naming a wrong or invented article: Apertus alone → Apertus + Belegt</p></div>
   <div class="kpi"><b>{M['trap_refused']['belegt']}/{M['trap_refused']['n']}</b><p>trap questions refused by Belegt ({M['trap_refused']['baseline']}/{M['trap_refused']['n']} by Apertus alone)</p></div>
   <div class="kpi"><b>0</b><p>outbound connections: Apertus runs locally, demo in a network namespace with no route out</p></div>
  </div>
  <div><img src="../img/landing.png" style="width:100%;height:78mm;object-fit:cover;object-position:top;border-radius:10pt;border:.6pt solid #1c02041f"></div>
  <p class="muted" style="margin:0">Code, data, evaluation and receipts: github.com/chessoren/swiss · Apache-2.0</p>
</section>
<h1>About the project</h1>
{md(story)}
<div class="shots"><img src="../img/answer_en.png"><img src="../img/answer_rm.png"><img src="../img/refusal.png"><img src="../img/receipt.png"></div>
<section class="pb"><h1>For judges and organisers</h1>{md(judges)}</section>
<section class="pb">{md(essai)}</section>
</body></html>"""
out = ROOT / "docs" / "submission" / "submission.html"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(doc)
print("wrote", out)
