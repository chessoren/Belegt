// Render docs/deck/deck.html → docs/deck/png/slide-NN.png (2400x1600, 3:2) + docs/deck/Belegt-deck.pdf
const { chromium } = await import(process.env.PLAYWRIGHT_MODULE || "playwright");
import fs from "node:fs";
import path from "node:path";
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const out = path.join(root, "docs/deck/png");
fs.mkdirSync(out, { recursive: true });
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1500, height: 1000 }, deviceScaleFactor: 1.6 });
await p.goto("file://" + path.join(root, "docs/deck/deck.html"));
await p.evaluate(() => document.fonts.ready);
await p.waitForTimeout(800);
const n = await p.locator(".slide").count();
for (let i = 0; i < n; i++) {
  await p.locator(".slide").nth(i).screenshot({ path: path.join(out, `slide-${String(i + 1).padStart(2, "0")}.png`) });
}
await p.addStyleTag({ content: "html,body{background:#fff}.slide{margin:0;page-break-after:always}" });
await p.pdf({ path: path.join(root, "docs/deck/Belegt-deck.pdf"), width: "1500px", height: "1000px", printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
await b.close();
console.log(n, "slides rendered");
