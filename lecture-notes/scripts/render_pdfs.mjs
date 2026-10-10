import { launch } from "puppeteer-core";
import { mkdir, readdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const htmlDir = path.join(root, "html");
const pdfDir = path.join(root, "pdf");
const chrome =
  process.env.CHROME_PATH ||
  "/usr/bin/google-chrome-stable";

const files = (await readdir(htmlDir))
  .filter((f) => f.endsWith(".html"))
  .sort();

await mkdir(pdfDir, { recursive: true });

const browser = await launch({
  executablePath: chrome,
  headless: "new",
  args: ["--no-sandbox", "--disable-gpu", "--font-render-hinting=none"],
});

try {
  for (const file of files) {
    const page = await browser.newPage();
    await page.setViewport({ width: 1240, height: 1754, deviceScaleFactor: 2 });
    const url = pathToFileURL(path.join(htmlDir, file)).href;
    await page.goto(url, { waitUntil: "load", timeout: 120000 });
    await page.evaluate(async () => {
      if (document.fonts?.ready) {
        await document.fonts.ready;
      }
      if (window.MathJax?.startup?.promise) {
        await window.MathJax.startup.promise;
      }
    });
    await new Promise((r) => setTimeout(r, 250));
    const out = path.join(pdfDir, file.replace(/\.html$/, ".pdf"));
    await page.pdf({
      path: out,
      format: "A4",
      printBackground: true,
      preferCSSPageSize: true,
      margin: { top: "0", right: "0", bottom: "0", left: "0" },
    });
    await page.close();
    console.log("wrote", path.relative(root, out));
  }
} finally {
  await browser.close();
}
