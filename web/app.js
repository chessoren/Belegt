/* Belegt front-end. No framework, no CDN, no tracker. */
(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const params = new URLSearchParams(location.search);
  const LANGS = ["de", "fr", "it", "rm"];

  /* ------------------------------------------------------------ i18n */
  const guess = () => "en"; // default interface language: English (switch with the FR/DE/IT/RM selector)
  let ui = params.get("ui") || (() => { try { return localStorage.getItem("belegt.ui"); } catch { return null; } })() || guess();
  if (!I18N[ui]) ui = "en";
  const t = (k, vars = {}) => {
    let s = (I18N[ui] && I18N[ui][k]) ?? I18N.fr[k] ?? k;
    for (const [a, b] of Object.entries(vars)) s = s.replaceAll(`{${a}}`, b);
    return s;
  };
  const tn = (k, n, vars = {}) => t(n === 1 ? k : k + "P", { n, ...vars }) || t(k, { n, ...vars });
  function applyI18n() {
    document.documentElement.lang = ui;
    $$("[data-i18n]").forEach((el) => (el.textContent = t(el.dataset.i18n)));
    $$("[data-i18n-html]").forEach((el) => (el.innerHTML = t(el.dataset.i18nHtml)));
    $$("[data-ui-lang]").forEach((s) => (s.value = ui));
    $$("[data-fedlex-link]").forEach((a) => (a.href = `https://www.fedlex.admin.ch/eli/cc/1999/404/${ui === "en" ? "en" : ui}`));
    $$("textarea[data-q]").forEach((ta) => { if (ta.id === "q-dock") ta.placeholder = t("askAnything"); });
    renderChart();
    renderNet();
  }
  $$("[data-ui-lang]").forEach((s) => s.addEventListener("change", () => {
    ui = s.value; try { localStorage.setItem("belegt.ui", ui); } catch {}
    applyI18n(); setPoster(posterIdx, true);
  }));

  /* --------------------------------------------------------- posters */
  const POSTERS = [
    { lang: "fr", greet: "Bonjour, la Suisse", num: "22", head: "Liberté de réunion", quote: "La liberté de réunion est garantie.", v: "", q: "Ai-je le droit de manifester dans la rue ?" },
    { lang: "de", greet: "Grüezi, Schweiz", num: "8", head: "Rechtsgleichheit", quote: "Alle Menschen sind vor dem Gesetz gleich.", v: "v-ink", q: "Haben Mann und Frau Anspruch auf gleichen Lohn?" },
    { lang: "it", greet: "Ciao, Svizzera", num: "4", head: "Lingue nazionali", quote: "Le lingue nazionali sono il tedesco, il francese, l’italiano e il romancio.", v: "v-paper", q: "La pena di morte è ammessa in Svizzera?" },
    { lang: "rm", greet: "Allegra, Svizra", num: "16", head: "Libertad d’opiniun e d’infurmaziun", quote: "La libertad d’opiniun e d’infurmaziun è garantida.", v: "", q: "Hai jau il dretg da demonstrar sin via?" },
  ];
  const posterEl = $("[data-posters]");
  posterEl.innerHTML = POSTERS.map((p, i) => `
    <div class="poster ${p.v}" data-i="${i}">
      <div class="grid-lines"></div>
      <span class="cross" aria-hidden="true">§</span>
      <div class="p-meta">${esc(p.head)}<br>${p.lang.toUpperCase()} · SR 101</div>
      <div class="p-quote">«${esc(p.quote)}»</div>
      <div class="p-num">Art.&nbsp;${p.num}</div>
    </div>`).join("");
  let posterIdx = 3, paused = false, timer = null;
  const greetEl = $("[data-greet]");
  function setPoster(i, instant = false) {
    posterIdx = (i + POSTERS.length) % POSTERS.length;
    $$(".poster", posterEl).forEach((p, j) => p.classList.toggle("on", j === posterIdx));
    const p = POSTERS[posterIdx];
    const heroQ = $("#q-hero");
    if (!heroQ.value) heroQ.placeholder = t("tryQ", { q: p.q });
    if (instant) { greetEl.textContent = p.greet; return; }
    greetEl.classList.add("out");
    setTimeout(() => { greetEl.textContent = p.greet; greetEl.classList.remove("out"); }, 420);
  }
  function startTimer() { clearInterval(timer); if (!paused) timer = setInterval(() => setPoster(posterIdx + 1), 5200); }
  $("[data-car=prev]").onclick = () => { setPoster(posterIdx - 1); startTimer(); };
  $("[data-car=next]").onclick = () => { setPoster(posterIdx + 1); startTimer(); };
  $("[data-car=pause]").onclick = (e) => {
    paused = !paused; startTimer();
    $("[data-pause-ico]").innerHTML = paused ? '<path d="M5 3.5v9l7.5-4.5z"/>' : '<rect x="4" y="3" width="2.6" height="10" rx="1"/><rect x="9.4" y="3" width="2.6" height="10" rx="1"/>';
  };

  const CHIPS = [
    ["EN", "Do I have the right to demonstrate in the street?"],
    ["RM", "Hai jau il dretg da demonstrar sin via?"],
    ["DE", "Wie viele Unterschriften braucht eine Volksinitiative?"],
    ["FR", "Ai-je le droit de manifester dans la rue ?"],
    ["EN", "Which article of the Swiss Constitution sets the maximum price of bread?"],
  ];
  $("[data-chips]").innerHTML = CHIPS.map(([l, q]) => `<button class="chip" type="button" data-ask="${esc(q)}"><b>${l}</b>${esc(q)}</button>`).join("");

  /* ---------------------------------------------------------- network */
  let net = null;
  function renderNet() {
    $$("[data-net]").forEach((pill) => {
      if (!net) { $("[data-net-label]", pill).textContent = t("netUnknown"); return; }
      pill.dataset.offline = String(!!net.offline);
      $("[data-net-label]", pill).textContent = net.offline ? t("netOffline") : t("netOnline");
      $("[data-net-count]", pill).textContent = "· " + tn("netCount", net.outbound_attempts);
    });
    const cap = $("[data-net-cap]");
    if (cap && net) cap.textContent = tn("netCount", net.outbound_attempts);
  }
  let status = null;
  async function pollStatus() {
    try {
      const r = await fetch("/api/status", { cache: "no-store" });
      status = await r.json(); net = status.network;
    } catch { net = null; }
    renderNet();
  }
  pollStatus(); setInterval(pollStatus, 2500);

  /* ------------------------------------------------------- mini chart */
  let summary = null;
  fetch("/data/eval-summary.json", { cache: "no-store" }).then((r) => (r.ok ? r.json() : null)).then((s) => { summary = s; renderChart(); }).catch(() => {});
  function renderChart() {
    const el = $("[data-mini-chart]");
    if (!el) return;
    if (!summary) { el.innerHTML = `<div class="muted">…</div>`; return; }
    const rows = [
      [t("chartTrap"), summary.chart.trap_refused.base, summary.chart.trap_refused.belegt],
      [t("chartWrong"), summary.chart.wrong_published.base, summary.chart.wrong_published.belegt],
      [t("chartLang"), summary.chart.lang_agree.base, summary.chart.lang_agree.belegt],
    ];
    el.innerHTML = rows.map(([l, b, u]) => `
      <div class="bar-row"><div class="bar-lbl"><span>${esc(l)}</span></div>
        <div class="bar"><i style="width:${Math.max(2, b)}%"></i></div>
        <div class="bar us"><i style="width:${Math.max(2, u)}%"></i></div>
        <div class="bar-lbl" style="color:var(--color-text-secondary);font-size:.75rem"><span>${b}%</span><b style="color:var(--color-red-600)">${u}%</b></div></div>`).join("") +
      `<div class="legend"><span><i style="background:var(--color-red-900-45)"></i>${esc(t("chartBase"))}</span><span><i style="background:var(--color-red-600)"></i>${esc(t("chartUs"))}</span></div>`;
  }

  /* ----------------------------------------------------------- sheet */
  const sheet = $("[data-sheet]"), scrim = $("[data-scrim]");
  let lastFocus = null;
  function openSheet(title, html) {
    lastFocus = document.activeElement;
    $("[data-sheet-title]").textContent = title;
    $("[data-sheet-body]").innerHTML = html;
    sheet.classList.add("on"); scrim.classList.add("on");
    $("[data-close]").focus();
  }
  function closeSheet() { sheet.classList.remove("on"); scrim.classList.remove("on"); lastFocus?.focus?.(); }
  $("[data-close]").onclick = closeSheet; scrim.onclick = closeSheet;
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeSheet(); });

  function page(name) {
    const P = PAGES[ui] || PAGES.fr;
    if (name === "menu") {
      const items = [["home", t("home")], ["how", t("howT")], ["privacy", t("privacyT")], ["numbers", t("numbersT")], ["limits", t("limitsT")], ["about", t("aboutT")]];
      return openSheet("", `<ul class="menu-list">${items.map(([k, l]) => `<li><button type="button" data-open="${k}">${esc(l)}</button></li>`).join("")}</ul>
        <div class="menu-note"><span class="brand-mark" aria-hidden="true" style="width:22px;height:22px;border-radius:5px"><svg viewBox="0 0 18 18" style="width:14px;height:14px"><path d="M3.2 5.2 0.8 9l2.4 3.8M7.2 5.2 4.8 9l2.4 3.8M10.8 5.2 13.2 9l-2.4 3.8M14.8 5.2 17.2 9l-2.4 3.8" stroke="#fff" stroke-width="1.9" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></span>${esc(t("menuNote"))}</div>`);
    }
    if (name === "home") { closeSheet(); goHome(); return; }
    if (name === "numbers") return openSheet(t("numbersT"), numbersHtml());
    const titles = { how: "howT", privacy: "privacyT", limits: "limitsT", about: "aboutT" };
    openSheet(t(titles[name]), P[name] || PAGES.fr[name]);
  }
  document.addEventListener("click", (e) => {
    const o = e.target.closest("[data-open]");
    if (o) { e.preventDefault(); page(o.dataset.open); return; }
    const a = e.target.closest("[data-ask]");
    if (a) { e.preventDefault(); ask(a.dataset.ask); return; }
    const art = e.target.closest("[data-article]");
    if (art) { e.preventDefault(); openArticle(art.dataset.article, art.dataset.lang, art.dataset.pid, art.dataset.quote); return; }
    const np = e.target.closest("[data-net]");
    if (np) { e.preventDefault(); openNet(); return; }
    const rc = e.target.closest("[data-receipt]");
    if (rc) { e.preventDefault(); openReceipt(receipts[rc.dataset.receipt]); return; }
  });

  function numbersHtml() {
    if (!summary) return `<div class="prose"><p>…</p></div>`;
    const s = summary;
    const row = (label, m) => `<tr><td>${esc(label)}</td><td class="num">${m.base}</td><td class="num"><b>${m.belegt}</b></td></tr>`;
    return `<div class="prose">
      <p>${esc(s.text[ui] || s.text.en)}</p>
      <table><thead><tr><th></th><th class="num">${esc(t("chartBase"))}</th><th class="num">${esc(t("chartUs"))}</th></tr></thead>
      <tbody>${s.table.map((r) => row(r.label[ui] || r.label.en, r)).join("")}</tbody></table>
      <p class="muted">${esc(s.footnote[ui] || s.footnote.en)}</p></div>`;
  }

  /* ------------------------------------------------------ network sheet */
  async function openNet() {
    await pollStatus();
    const n = net || {}, m = status?.model || {}, c = status?.corpus || {};
    const yes = (b) => (b ? "✓" : "✗");
    const row = (k, v) => `<dt>${esc(k)}</dt><dd>${v}</dd>`;
    openSheet(t("netTitle"), `
      <div class="receipt"><div class="r-head"><div><div class="muted">${esc(t("netNow"))}</div>
        <div class="decision">${esc(n.offline ? t("netOffline") : t("netOnline"))}</div></div>
        <div style="text-align:right"><div class="r-id" style="font-size:2rem">${n.outbound_attempts ?? 0}</div><div class="muted">${esc(t("netBlocked"))}</div></div></div>
      <dl>
        ${row(t("netRoute"), n.default_route ? esc(t("netYes")) : `<b>${esc(t("netNone"))}</b>`)}
        ${row(t("netLoop"), `${n.loopback_calls ?? 0}`)}
        ${row(t("rcModel"), `${esc(m.model || "")}<br><span class="muted">${esc(m.url || "")} · ${yes(m.ok)}</span>`)}
        ${row(t("rcModelHash"), `<span class="mono">${esc((m.sha256 || "…").slice(0, 32))}…</span>`)}
        ${row(t("rcLaw"), `SR ${esc(c.sr || "101")} · ${esc(String(c.version || "").replace(/(\d{4})(\d{2})(\d{2})/, "$3.$2.$1"))} · DE ${c.languages?.de ?? ""} · FR ${c.languages?.fr ?? ""} · IT ${c.languages?.it ?? ""} · RM ${c.languages?.rm ?? ""}`)}
        ${row(t("rcTextHash"), `<span class="mono">${esc((c.fingerprint || "").slice(0, 32))}…</span>`)}
        ${row("PID", `${n.pid ?? ""}`)}
      </dl>
      <p class="muted" style="margin:14px 0 0">${esc(t("netExplain"))}</p></div>`);
  }

  /* ---------------------------------------------------------- article */
  const artCache = {};
  async function openArticle(article, lang, pid, quote) {
    lang = LANGS.includes(lang) ? lang : (LANGS.includes(ui) ? ui : "fr");
    let data = artCache[article];
    if (!data) {
      try { data = artCache[article] = await (await fetch(`/api/article?id=${encodeURIComponent(article)}`)).json(); }
      catch { return; }
    }
    const render = (l) => {
      const paras = data.languages[l] || [];
      const head = paras[0] ? `Art. ${paras[0].art_num}` : article;
      const html = `
        <div class="tabs" role="tablist">${LANGS.map((x) => `<button class="tab" role="tab" aria-selected="${x === l}" data-tab="${x}">${x.toUpperCase()}</button>`).join("")}</div>
        <div><p class="muted" style="margin:0 0 4px">${esc(paras[0]?.heading || "")}</p><h4 class="art-title">${esc(head)}</h4></div>
        <div>${paras.map((p) => {
          let txt = esc(p.text);
          const hit = p.id === pid;
          if (hit && quote && l === lang) {
            const i = p.text.replace(/[’‘]/g, "'").replace(/[«»“”„]/g, '"').toLowerCase().indexOf(quote.toLowerCase());
            if (i >= 0) txt = esc(p.text.slice(0, i)) + "<mark>" + esc(p.text.slice(i, i + quote.length)) + "</mark>" + esc(p.text.slice(i + quote.length));
          }
          return `<div class="art-para ${hit ? "hit" : ""}">${p.para_num ? `<sup>${esc(p.para_num)}</sup>` : ""}${txt}</div>`;
        }).join("")}</div>
        <p class="muted">${esc(t("officialText"))} · <a class="link" href="${esc(data.urls[l])}#${esc(article)}" rel="noopener" target="_blank">fedlex.admin.ch ↗</a></p>`;
      openSheet(head, html);
      $$("[data-tab]").forEach((b) => (b.onclick = () => render(b.dataset.tab)));
    };
    render(lang);
  }

  /* ---------------------------------------------------------- receipt */
  const receipts = {};
  const CK = { verbatim_quotes: "ckVerbatim", no_unproven_article_numbers: "ckNoUnproven", citation_or_silence: "ckSilence", cross_language_agreement: "ckLangs" };
  const ICON_OK = '<svg viewBox="0 0 16 16" fill="none"><path d="m3.5 8.5 3 3 6-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  const ICON_WARN = '<svg viewBox="0 0 16 16" fill="none"><path d="M8 4.5v4.5M8 11.5v.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>';
  function openReceipt(r) {
    if (!r) return;
    const short = (h) => (h ? h.slice(0, 12) + "…" + h.slice(-6) : "—");
    const nw = r.network || {};
    const html = `
      <div class="receipt" id="receipt-print">
        <div class="r-head"><div><div class="muted">${esc(t("rcTitle"))}</div><div class="decision">${esc(r.decision === "answered" ? t("rcAnswered") : t("rcAbstained"))}</div></div>
          <div style="text-align:right"><div class="r-id">${esc(r.receipt_id)}</div><div class="muted">${esc(new Date(r.issued_at).toLocaleString(ui === "en" ? "en-GB" : ui + "-CH"))}</div></div></div>
        <dl>
          <dt>${esc(t("rcQuestion"))}</dt><dd>${esc(r.question)} <span class="muted">(${esc(r.language)})</span></dd>
          <dt>${esc(t("rcModel"))}</dt><dd>${esc(r.model.name)}<br><span class="muted">${esc(r.model.runtime)} · temp ${r.model.temperature} · seed ${r.model.seed}</span></dd>
          <dt>${esc(t("rcModelHash"))}</dt><dd class="mono">${esc(short(r.model.sha256))}</dd>
          <dt>${esc(t("rcLaw"))}</dt><dd>SR ${esc(r.law.sr)} · ${esc(r.law.title)}</dd>
          <dt>${esc(t("rcVersion"))}</dt><dd>${esc(r.law.version.replace(/(\d{4})(\d{2})(\d{2})/, "$3.$2.$1"))} · ${esc(r.law.evidence_language.toUpperCase())}</dd>
          <dt>${esc(t("rcTextHash"))}</dt><dd class="mono">${esc(short(r.law.text_sha256))}</dd>
          <dt>${esc(t("rcEvidence"))}</dt><dd>${r.evidence.length ? r.evidence.map((e) => `<b>${esc(e.label)}</b> «${esc(e.quote)}» <span class="mono muted">${esc(e.quote_sha256.slice(0, 8))}</span>`).join("<br>") : esc(t("rcNone"))}</dd>
          <dt>${esc(t("rcNetwork"))}</dt><dd>${esc(nw.offline ? t("rcOffline") : t("rcOnline"))} · <b>${nw.outbound_attempts ?? 0}</b> ${esc(t("rcOutbound"))}</dd>
          <dt>${esc(t("rcDuration"))}</dt><dd>${esc(r.duration_seconds)} ${esc(t("seconds"))}</dd>
        </dl>
        <ul class="checks">${r.checks.map((c) => `<li><span class="${c.passed ? "pass" : "fail"}">${c.passed ? ICON_OK : ICON_WARN}</span><code>${esc(c.rule)}</code><span>${esc(t(CK[c.name] || c.name))} <span class="muted">· ${esc(c.detail)}</span></span></li>`).join("")}</ul>
      </div>
      <div class="actions"><button class="btn btn-primary btn-sm" type="button" data-dl>${esc(t("rcDownload"))}</button><button class="btn btn-secondary btn-sm" type="button" data-print>${esc(t("rcPrint"))}</button></div>`;
    openSheet(t("receipt") + " " + r.receipt_id, html);
    $("[data-dl]").onclick = () => {
      const blob = new Blob([JSON.stringify(r, null, 2)], { type: "application/json" });
      const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = `${r.receipt_id}.json`; a.click();
      setTimeout(() => URL.revokeObjectURL(a.href), 2000);
    };
    $("[data-print]").onclick = () => window.print();
  }

  /* ------------------------------------------------------------- chat */
  const thread = $("[data-thread]");
  function goHome() { document.body.dataset.view = "landing"; history.pushState({}, "", "/"); window.scrollTo(0, 0); }
  $("[data-home]").onclick = (e) => { e.preventDefault(); goHome(); };
  window.addEventListener("popstate", () => { if (!location.search.includes("q=")) document.body.dataset.view = "landing"; });

  $$("[data-composer]").forEach((form) => {
    const ta = $("textarea", form);
    ta.addEventListener("input", () => { ta.style.height = "auto"; ta.style.height = Math.min(160, ta.scrollHeight) + "px"; });
    ta.addEventListener("keydown", (e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); form.requestSubmit(); } });
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const q = ta.value.trim() || (form.dataset.composer === "hero" ? POSTERS[posterIdx].q : "");
      if (!q) return;
      ta.value = ""; ta.style.height = "auto";
      ask(q);
    });
  });

  const STEP_KEYS = { understand: ["stUnderstand", "ai"], retrieve: ["stRetrieve", "code"], draft: ["stDraft", "ai"], verify: ["stVerify", "code"] };
  const SPIN = '<span class="spinner"></span>';
  const DONE = '<svg viewBox="0 0 18 18" fill="none"><circle cx="9" cy="9" r="8" fill="var(--color-verified-surface)"/><path d="m5.5 9.2 2.4 2.4 4.6-5" stroke="var(--color-verified)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  const PEND = '<svg viewBox="0 0 18 18" fill="none"><circle cx="9" cy="9" r="7.2" stroke="var(--color-border-tertiary)" stroke-width="1.6"/></svg>';

  let busy = false;
  async function ask(question) {
    if (busy) return;
    busy = true;
    document.body.dataset.view = "chat";
    if (!location.search.includes("q=")) history.pushState({}, "", "/?q=" + encodeURIComponent(question));
    closeSheet();
    const u = document.createElement("div");
    u.className = "msg-user"; u.textContent = question;
    thread.appendChild(u);
    const bot = document.createElement("div");
    bot.className = "msg-bot";
    bot.innerHTML = `<div class="steps">${Object.entries(STEP_KEYS).map(([k, [label, who]]) => `
      <div class="step" data-step="${k}"><span class="ico">${PEND}</span><span>${esc(t(label))}<span class="who ${who === "ai" ? "ai" : ""}">${esc(t(who === "ai" ? "whoAI" : "whoCode"))}</span></span><span class="t"></span></div>
      <div class="detail" data-detail="${k}" hidden></div>`).join("")}</div>`;
    thread.appendChild(bot);
    window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
    const started = {}, timers = {};
    const setStep = (k, state, secs) => {
      const el = $(`[data-step="${k}"]`, bot); if (!el) return;
      el.classList.toggle("active", state === "start"); el.classList.toggle("done", state === "done");
      $(".ico", el).innerHTML = state === "start" ? SPIN : state === "done" ? DONE : PEND;
      if (state === "start") {
        started[k] = performance.now();
        timers[k] = setInterval(() => { $(".t", el).textContent = ((performance.now() - started[k]) / 1000).toFixed(0) + " s"; }, 250);
      } else if (state === "done") {
        clearInterval(timers[k]);
        $(".t", el).textContent = secs != null ? (secs < 1 ? secs.toFixed(2) : secs.toFixed(1)) + " s" : "";
      }
    };
    const handle = (ev) => {
      if (ev.type === "step" && STEP_KEYS[ev.step]) {
        setStep(ev.step, ev.status, ev.seconds);
        if (ev.step === "understand" && ev.status === "done" && ev.queries) {
          const d = $('[data-detail="understand"]', bot); d.hidden = false;
          d.innerHTML = LANGS.map((l) => `<code>${l.toUpperCase()}</code> ${esc(ev.queries[l])}`).join(" &nbsp; ");
        }
        if (ev.step === "retrieve" && ev.status === "done" && ev.candidates) {
          const d = $('[data-detail="retrieve"]', bot); d.hidden = false;
          d.innerHTML = esc(t("candidates")) + " : " + ev.candidates.map((c) => `<code>${esc(c)}</code>`).join(" ");
        }
      } else if (ev.type === "result") {
        Object.values(timers).forEach(clearInterval);
        renderResult(bot, ev);
      } else if (ev.type === "error") {
        Object.values(timers).forEach(clearInterval);
        bot.insertAdjacentHTML("beforeend", `<div class="refusal"><p>${esc(t("errorT"))}</p><p class="muted">${esc(ev.message || "")}</p></div>`);
      }
    };
    try {
      if (params.get("replay")) await replay(params.get("replay"), question, handle);
      else await stream(question, handle);
    } catch (e) {
      handle({ type: "error", message: String(e) });
    } finally {
      busy = false;
      pollStatus();
    }
  }

  async function stream(question, onEvent) {
    const r = await fetch("/api/ask", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ question }) });
    if (!r.ok || !r.body) throw new Error("HTTP " + r.status);
    const reader = r.body.getReader(); const dec = new TextDecoder(); let buf = "";
    for (;;) {
      const { value, done } = await reader.read();
      if (done) break;
      buf += dec.decode(value, { stream: true });
      let i;
      while ((i = buf.indexOf("\n\n")) >= 0) {
        const chunk = buf.slice(0, i); buf = buf.slice(i + 2);
        const line = chunk.split("\n").find((l) => l.startsWith("data:"));
        if (line) onEvent(JSON.parse(line.slice(5)));
      }
    }
  }

  /* Replays a recorded real run (web/data/replays/<name>.json); used for docs screenshots. */
  async function replay(name, question, onEvent) {
    const evs = await (await fetch(`/data/replays/${encodeURIComponent(name)}.json`)).json();
    const speed = +(params.get("speed") || 20);
    for (const ev of evs) {
      if (ev.type === "step" && ev.status === "done" && ev.seconds) await new Promise((r) => setTimeout(r, (ev.seconds * 1000) / speed));
      else await new Promise((r) => setTimeout(r, 120));
      onEvent(ev);
    }
  }

  function markQuote(text, quote, span) {
    if (span && text.slice(span[0], span[1]).replace(/[’‘]/g, "'").replace(/[«»“”„]/g, '"') === quote) {
      return esc(text.slice(0, span[0])) + "<mark>" + esc(text.slice(span[0], span[1])) + "</mark>" + esc(text.slice(span[1]));
    }
    return esc(text);
  }

  function renderResult(bot, r) {
    receipts[r.receipt.receipt_id] = r.receipt;
    const steps = $(".steps", bot);
    steps.insertAdjacentHTML("afterend", `<div data-res></div>`);
    const res = $("[data-res]", bot);
    if (r.decision === "answered") {
      const cites = r.citations;
      const allLangsOk = r.consistency_ok;
      const perLang = {};
      LANGS.forEach((l) => (perLang[l] = r.consistency.every((c) => c.found_in[l])));
      const missing = LANGS.filter((l) => !perLang[l]);
      const agree = LANGS.length - missing.length;
      const sentences = (r.sentences && r.sentences.length ? r.sentences : [{ text: r.answer, support: { kind: "quoted" } }]);
      const chips = cites.map((c) => `<button class="cite-chip" type="button" data-article="${esc(c.article)}" data-lang="${esc(c.lang)}" data-pid="${esc(c.id)}" data-quote="${esc(c.quote)}">${ICON_OK}${esc(c.label)}</button>`).join("");
      const notes = [];
      if (r.rejected?.length) notes.push(esc(t("verRejected", { n: r.rejected.length })));
      if (r.removed_sentences?.length) notes.push(esc(t("verRemoved", { n: r.removed_sentences.length })));
      const first = cites[0];
      const par = first ? r.parallel[first.id] : null;
      res.innerHTML = `
        <div class="msg-bot">
          <div class="verified-head">
            <span class="badge ok">${ICON_OK}${esc(tn("verifiedBadge", cites.length))}</span>
            ${allLangsOk ? `<span class="badge neutral">${esc(t("langsAgree", { a: agree }))}</span>` : `<span class="badge warn">${ICON_WARN}${esc(t("langsAgree", { a: agree }))}</span>`}
          </div>
          <div class="answer"><p>${sentences.map((s) => s.support.kind === "inference" ? `<span class="s-inference" title="${esc(t("inferenceTip"))}">${esc(s.text)}</span>` : esc(s.text)).join(" ")} ${chips}</p></div>
          ${notes.length ? `<div class="verifier-note">${notes.join("<br>")}</div>` : ""}
          <div class="evidence">${cites.map((c) => `
            <button class="ev-card" type="button" data-article="${esc(c.article)}" data-lang="${esc(c.lang)}" data-pid="${esc(c.id)}" data-quote="${esc(c.quote)}">
              <span class="ev-top"><span class="ev-label">${esc(c.label)}</span><span class="ev-heading">${esc(c.heading)}</span></span>
              <span class="ev-text">${markQuote(c.para_text || c.quote, c.quote, c.span)}</span>
              <span class="ev-foot"><span class="badge ok" style="height:22px;font-size:.6875rem">${ICON_OK}${esc(t("foundVerbatim"))}</span>${esc(t("officialText"))}</span>
            </button>`).join("")}</div>
          <div class="langs">
            <div class="langs-head"><h4>${esc(t("langsHead"))}</h4>
              <div class="lang-dots">${LANGS.map((l) => `<span class="lang-dot ${perLang[l] ? "ok" : "miss"}">${perLang[l] ? ICON_OK : ICON_WARN}${l.toUpperCase()}</span>`).join("")}</div></div>
            ${missing.length ? `<div class="verifier-note">${esc(t("langsDiverge", { langs: missing.map((l) => t("lang")[l]).join(", ") }))}</div>` : ""}
            ${par ? `<div class="parallel">${LANGS.map((l) => par[l] ? `<div class="par ${l === r.evidence_lang ? "q" : ""}"><b>${l.toUpperCase()} · ${esc(par[l].label)}</b>${esc(par[l].text)}</div>` : "").join("")}</div>` : ""}
          </div>
          <div class="actions">
            <button class="btn btn-secondary btn-sm" type="button" data-receipt="${esc(r.receipt.receipt_id)}">${esc(t("receipt"))} · ${esc(r.receipt.receipt_id)}</button>
            ${first ? `<button class="btn btn-ghost btn-sm" type="button" data-article="${esc(first.article)}" data-lang="${esc(first.lang)}" data-pid="${esc(first.id)}" data-quote="${esc(first.quote)}">${esc(t("openArticle"))}</button>` : ""}
            <button class="btn btn-ghost btn-sm" type="button" data-copy>${esc(t("copy"))}</button>
          </div>
        </div>`;
      $("[data-copy]", res).onclick = (e) => {
        const txt = r.answer + "\n\n" + cites.map((c) => `${c.label}: «${c.quote}»`).join("\n") + `\n\n${r.receipt.receipt_id}`;
        navigator.clipboard?.writeText(txt).then(() => (e.target.textContent = t("copied")));
      };
    } else {
      res.innerHTML = `
        <div class="refusal">
          <h3><svg viewBox="0 0 26 26" fill="none"><circle cx="13" cy="13" r="11" stroke="currentColor" stroke-width="2"/><path d="M8 13h10" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>${esc(t("refusalT"))}</h3>
          <p>${esc(t("refusalP"))}</p>
          <div class="nearest"><span class="t">${esc(t("nearestT"))}</span>
            <div class="near-list">${r.nearest.map((n) => `<button class="near" type="button" data-article="${esc(n.article)}" data-lang="${esc(r.evidence_lang)}" data-pid="${esc(n.id)}"><b>${esc(n.label)}</b><span>${esc(n.heading)}</span></button>`).join("")}</div></div>
          <p class="muted">${esc(t("cannotClaim"))}</p>
        </div>
        <div class="actions"><button class="btn btn-secondary btn-sm" type="button" data-receipt="${esc(r.receipt.receipt_id)}">${esc(t("receipt"))} · ${esc(r.receipt.receipt_id)}</button></div>`;
    }
    setTimeout(() => res.scrollIntoView({ behavior: "smooth", block: "start" }), 60);
  }

  /* ----------------------------------------------------------- reveal */
  const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }), { threshold: 0.15 });
  $$(".reveal").forEach((el) => io.observe(el));
  if (params.get("static")) $$(".reveal").forEach((el) => el.classList.add("in"));

  applyI18n();
  setPoster(params.get("poster") ? +params.get("poster") : 3, true);
  startTimer();
  if (params.get("still")) { paused = true; clearInterval(timer); }
  const q0 = params.get("q");
  if (q0) ask(q0);
})();
