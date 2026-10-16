// UI screenshots for README / deck / PDF, rendered from recorded real runs (web/data/replays).
//   UI=en node scripts/screenshots.mjs docs/img
const { chromium } = await import(process.env.PLAYWRIGHT_MODULE || "playwright");
const OUT = process.argv[2] || "docs/img";
const UI = process.env.UI || "en";
const B = process.env.BELEGT_URL || "http://127.0.0.1:8080";
const b = await chromium.launch();
const q = (s) => encodeURIComponent(s);

async function shot(name, url, { w = 1440, h = 900, act = null } = {}) {
  const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2 });
  await p.goto(B + url, { waitUntil: "networkidle" });
  await p.waitForTimeout(2500);
  if (act) await act(p);
  await p.screenshot({ path: `${OUT}/${name}.png` });
  await p.close();
}
const atRes = async (p) => { await p.waitForSelector("[data-res]", { timeout: 60000 }); await p.waitForTimeout(800); await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(400); };
const ask = (replay, question) => `/?ui=${UI}&replay=${replay}&speed=80&q=${q(question)}`;

const DEMO = "Do I have the right to demonstrate in the street?";
const BREAD = "Which article of the Swiss Constitution sets the maximum price of bread?";
const RM = "Hai jau il dretg da demonstrar sin via?";

await shot("landing", `/?ui=${UI}&static=1&still=1&poster=0`);
await shot("mobile", `/?ui=${UI}&static=1&still=1&poster=3`, { w: 390, h: 844 });
await shot("answer_en", ask("demonstrate_en", DEMO), { h: 1500, act: atRes });
await shot("answer_rm", ask("romanche", RM), { h: 1700, act: atRes });
await shot("refusal", ask("bread_en", BREAD), { h: 1000, act: atRes });
await shot("receipt", ask("demonstrate_en", DEMO), { h: 1000, act: async (p) => { await atRes(p); await p.click("[data-receipt]"); await p.waitForTimeout(900); } });
await shot("article", ask("demonstrate_en", DEMO), { act: async (p) => { await atRes(p); await p.click(".ev-card"); await p.waitForTimeout(1500); } });
await shot("network", `/?ui=${UI}&static=1&still=1`, { act: async (p) => { await p.click(".site-header [data-net]"); await p.waitForTimeout(1200); } });
await b.close();
console.log("screenshots ok");
