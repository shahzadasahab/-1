import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { chromium } from "playwright";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(__dirname, "..");
const htmlDir = path.join(root, "dist", "html");
const pdfDir = path.join(root, "dist", "pdf");
const assetsDir = path.join(root, "assets");

fs.mkdirSync(pdfDir, { recursive: true });

const files = fs.readdirSync(htmlDir).filter((f) => f.endsWith(".html")).sort();

const browser = await chromium.launch({ headless: true });

for (const file of files) {
  const page = await browser.newPage();
  const htmlPath = path.join(htmlDir, file);
  const url = "file://" + htmlPath;

  await page.goto(url, { waitUntil: "networkidle", timeout: 120_000 });
  await page.evaluate(async () => {
    if (window.MathJax?.startup?.promise) {
      await window.MathJax.startup.promise;
      if (window.MathJax.typesetPromise) {
        await window.MathJax.typesetPromise();
      }
    }
  });

  const pdfName = file.replace(/\.html$/, ".pdf");
  await page.pdf({
    path: path.join(pdfDir, pdfName),
    format: "A4",
    printBackground: true,
    margin: { top: "12mm", bottom: "14mm", left: "10mm", right: "10mm" },
  });
  console.log("PDF", pdfName);
  await page.close();
}

await browser.close();
console.log(`Done — ${files.length} PDFs in dist/pdf/`);
