// Screenshots taken inside the offline namespace (network panel shows the real offline state).
const { chromium } = await import(process.env.PLAYWRIGHT_MODULE || "playwright");
const OUT = process.argv[2];
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
await p.goto("http://127.0.0.1:8080/?ui=fr&static=1&still=1", { waitUntil: "networkidle" });
await p.waitForTimeout(3000);
await p.click(".site-header [data-net]"); await p.waitForTimeout(1200);
await p.screenshot({ path: `${OUT}/network.png` });
await p.keyboard.press("Escape");
await p.goto("http://127.0.0.1:8080/?ui=en&static=1&still=1&poster=0", { waitUntil: "networkidle" });
await p.waitForTimeout(3000);
await p.screenshot({ path: `${OUT}/landing.png` });
await b.close();
