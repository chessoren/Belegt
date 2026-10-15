// docs/submission/submission.html → docs/submission/Belegt-submission.pdf (A4)
const { chromium } = await import(process.env.PLAYWRIGHT_MODULE || "playwright");
import path from "node:path";
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const b = await chromium.launch();
const p = await b.newPage();
await p.goto("file://" + path.join(root, "docs/submission/submission.html"), { waitUntil: "load" });
await p.evaluate(() => document.fonts.ready);
await p.pdf({ path: path.join(root, "docs/submission/Belegt-submission.pdf"), format: "A4", printBackground: true,
  displayHeaderFooter: true, headerTemplate: "<span></span>",
  footerTemplate: '<div style="font-size:7pt;width:100%;text-align:center;color:#999;font-family:sans-serif">Belegt · Hack Apertus 2026 · <span class="pageNumber"></span>/<span class="totalPages"></span></div>',
  margin: { top: "18mm", bottom: "20mm", left: "18mm", right: "18mm" } });
await b.close();
console.log("pdf ok");
