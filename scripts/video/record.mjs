// Records the real app, live, scene by scene (CDP screencast → JPEG frames + timestamps).
// Run inside the offline namespace:  scripts/offline_demo.sh node scripts/video/record.mjs OUT_DIR
const { chromium } = await import(process.env.PLAYWRIGHT_MODULE || "playwright");
import fs from "node:fs";
import path from "node:path";

const OUT = process.argv[2] || "video-frames";
const BASE = process.env.BELEGT_URL || "http://127.0.0.1:8080";
const W = 1920, H = 1080;
fs.mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || undefined });
const log = [];

async function scene(name, fn) {
  const dir = path.join(OUT, name);
  fs.mkdirSync(dir, { recursive: true });
  const ctx = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1, locale: "fr-CH" });
  const page = await ctx.newPage();
  const cdp = await ctx.newCDPSession(page);
  const frames = [];
  let n = 0;
  cdp.on("Page.screencastFrame", async (f) => {
    const file = path.join(dir, `f${String(n++).padStart(6, "0")}.jpg`);
    fs.writeFileSync(file, Buffer.from(f.data, "base64"));
    frames.push({ file: path.basename(file), t: f.metadata.timestamp });
    try { await cdp.send("Page.screencastFrameAck", { sessionId: f.sessionId }); } catch {}
  });
  const t0 = Date.now() / 1000;
  const marks = [];
  const mark = (label) => { marks.push({ label, t: Date.now() / 1000 }); console.log(name, label, (Date.now() / 1000 - t0).toFixed(1)); };
  await page.goto(BASE + "/?ui=fr&still=1", { waitUntil: "networkidle" });
  await cdp.send("Page.startScreencast", { format: "jpeg", quality: 92, maxWidth: W, maxHeight: H, everyNthFrame: 1 });
  mark("start");
  try { await fn(page, mark); } catch (e) { console.error(name, e); }
  mark("end");
  await page.waitForTimeout(300);
  await cdp.send("Page.stopScreencast");
  fs.writeFileSync(path.join(dir, "frames.json"), JSON.stringify({ frames, marks }, null, 1));
  log.push({ name, marks });
  await ctx.close();
}

const typeInto = async (page, sel, text) => {
  await page.click(sel);
  await page.keyboard.type(text, { delay: 55 });
};
const waitResult = async (page, mark) => {
  await page.waitForSelector("[data-res]", { timeout: 600000 });
  mark("result");
};

// A — landing
await scene("a_landing", async (page, mark) => {
  await page.waitForTimeout(2500);
  await page.click("[data-car=next]"); await page.waitForTimeout(1800);
  await page.click("[data-car=next]"); await page.waitForTimeout(1800);
  await page.click("[data-car=next]"); await page.waitForTimeout(1800);
  await page.click("[data-car=next]"); await page.waitForTimeout(1500);
  mark("scroll");
  for (let y = 0; y < 3300; y += 30) { await page.mouse.wheel(0, 30); await page.waitForTimeout(16); }
  await page.waitForTimeout(1500);
  for (let y = 0; y < 3300; y += 60) { await page.mouse.wheel(0, -60); await page.waitForTimeout(10); }
  await page.waitForTimeout(1000);
});

// B — French question
await scene("b_fr", async (page, mark) => {
  await page.waitForTimeout(800);
  mark("type");
  await typeInto(page, "#q-hero", "Ai-je le droit de manifester dans la rue ?");
  await page.waitForTimeout(500);
  mark("submit");
  await page.keyboard.press("Enter");
  await waitResult(page, mark);
  await page.waitForTimeout(2500);
  await page.mouse.wheel(0, 380); await page.waitForTimeout(2200);
  mark("open-evidence");
  await page.click(".ev-card"); await page.waitForTimeout(3500);
  mark("tab-de");
  await page.click('[data-tab="de"]'); await page.waitForTimeout(1800);
  await page.click('[data-tab="rm"]'); await page.waitForTimeout(1800);
  await page.keyboard.press("Escape"); await page.waitForTimeout(800);
});

// C — Romansh
await scene("c_rm", async (page, mark) => {
  await page.waitForTimeout(600);
  mark("type");
  await typeInto(page, "#q-hero", "Hai jau il dretg da demonstrar sin via?");
  await page.waitForTimeout(400);
  mark("submit");
  await page.keyboard.press("Enter");
  await waitResult(page, mark);
  await page.waitForTimeout(2000);
  await page.mouse.wheel(0, 520); await page.waitForTimeout(4000);
});

// D — network proof + a new question, offline
await scene("d_net", async (page, mark) => {
  await page.waitForTimeout(800);
  mark("open-net");
  await page.click(".site-header [data-net]"); await page.waitForTimeout(5000);
  await page.keyboard.press("Escape"); await page.waitForTimeout(600);
  mark("type");
  await typeInto(page, "#q-hero", "Wie viele Unterschriften braucht eine Volksinitiative?");
  mark("submit");
  await page.keyboard.press("Enter");
  await waitResult(page, mark);
  await page.waitForTimeout(3500);
});

// E — trap question, refusal, receipt
await scene("e_trap", async (page, mark) => {
  await page.waitForTimeout(600);
  mark("type");
  await typeInto(page, "#q-hero", "Quel article de la Constitution fixe le prix maximum du pain ?");
  mark("submit");
  await page.keyboard.press("Enter");
  await waitResult(page, mark);
  await page.waitForTimeout(4000);
  mark("receipt");
  await page.click("[data-receipt]"); await page.waitForTimeout(5500);
  await page.keyboard.press("Escape"); await page.waitForTimeout(600);
});

// F — numbers
await scene("f_numbers", async (page, mark) => {
  await page.waitForTimeout(600);
  await page.evaluate(() => document.querySelector("[data-mini-chart]").scrollIntoView({ block: "center" }));
  await page.waitForTimeout(2500);
  mark("numbers");
  await page.click('[data-open="numbers"]'); await page.waitForTimeout(5000);
});

fs.writeFileSync(path.join(OUT, "log.json"), JSON.stringify(log, null, 1));
await browser.close();
