#!/usr/bin/env node
/**
 * Render lecture HTML (MathJax + embedded SVG + flexbox) to PDF via headless Chrome.
 */
import puppeteer from "puppeteer";
import { PDFDocument } from "pdf-lib";
import { fileURLToPath } from "url";
import path from "path";
import fs from "fs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(__dirname, "..");
const outDir = path.join(root, "output");

const targets = [
  { html: "class-xi-lecture-notes.html", pdf: "IT-Lecture-Notes-Class-XI.pdf" },
  { html: "class-xii-lecture-notes.html", pdf: "IT-Lecture-Notes-Class-XII.pdf" },
];

async function renderPdf(browser, htmlName, pdfName) {
  const htmlPath = path.join(root, htmlName);
  if (!fs.existsSync(htmlPath)) {
    console.warn(`Skip missing: ${htmlName}`);
    return null;
  }
  const page = await browser.newPage();
  const fileUrl = "file://" + htmlPath.split(path.sep).join("/");
  await page.goto(fileUrl, { waitUntil: "networkidle0", timeout: 120000 });
  await page.waitForFunction(() => {
    const mj = window.MathJax;
    if (!mj?.startup?.promise) return true;
    return mj.startup.promise.then(() => {
      if (mj.typesetPromise) return mj.typesetPromise();
      return true;
    });
  }, { timeout: 90000 }).catch(() => {});
  await page.evaluate(async () => {
    if (window.MathJax?.typesetPromise) {
      await window.MathJax.typesetPromise();
    }
  });
  await new Promise((r) => setTimeout(r, 500));
  const pdfPath = path.join(outDir, pdfName);
  await page.pdf({
    path: pdfPath,
    format: "A4",
    printBackground: true,
    margin: { top: "12mm", right: "12mm", bottom: "14mm", left: "12mm" },
  });
  await page.close();
  console.log("Wrote", pdfPath);
  return pdfPath;
}

async function mergePdfs(partPaths, outName) {
  const merged = await PDFDocument.create();
  for (const p of partPaths) {
    if (!p || !fs.existsSync(p)) continue;
    const bytes = fs.readFileSync(p);
    const doc = await PDFDocument.load(bytes);
    const pages = await merged.copyPages(doc, doc.getPageIndices());
    pages.forEach((page) => merged.addPage(page));
  }
  const outPath = path.join(outDir, outName);
  fs.writeFileSync(outPath, await merged.save());
  console.log("Wrote", outPath);
}

async function main() {
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await puppeteer.launch({
    headless: "new",
    args: ["--no-sandbox", "--disable-setuid-sandbox", "--font-render-hinting=none"],
  });
  try {
    const rendered = [];
    for (const t of targets) {
      rendered.push(await renderPdf(browser, t.html, t.pdf));
    }
    await mergePdfs(rendered.filter(Boolean), "IT-Lecture-Notes-Complete.pdf");
  } finally {
    await browser.close();
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
