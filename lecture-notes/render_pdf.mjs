// Rebuild the PDF after editing the HTML:
//   npm install --prefix /tmp/pdftools puppeteer-core
//   node lecture-notes/render_pdf.mjs
// Chrome must already be installed. MathJax is loaded from the CDN while printing,
// then stored in the PDF as SVG.
import puppeteer from "/tmp/pdftools/node_modules/puppeteer-core/lib/esm/puppeteer/puppeteer-core.js";
import path from "node:path";
import { pathToFileURL } from "node:url";

const htmlPath = path.resolve("/workspace/lecture-notes/grade-xii-cs-lecture-notes.html");
const pdfPath = path.resolve("/workspace/lecture-notes/Grade-XII-Computer-Science-Lecture-Notes.pdf");

const browser = await puppeteer.launch({
  executablePath: "/usr/bin/google-chrome",
  headless: true,
  args: ["--no-sandbox", "--disable-dev-shm-usage", "--allow-file-access-from-files"],
});

try {
  const page = await browser.newPage();
  page.setDefaultNavigationTimeout(120000);
  await page.goto(pathToFileURL(htmlPath).href, { waitUntil: "networkidle0", timeout: 120000 });
  await page.waitForFunction(() => window.mathjaxDone === true, { timeout: 60000 });
  await page.pdf({
    path: pdfPath,
    format: "A4",
    printBackground: true,
    preferCSSPageSize: false,
    displayHeaderFooter: true,
    headerTemplate: `
      <div style="font-size:8px; width:100%; padding:0 12mm; color:#5c6b7a; font-family:Inter,sans-serif; display:flex; justify-content:space-between;">
        <span>Grade XII · Computer Science · Lecture Notes</span>
        <span>SVG diagrams · MathJax · flexbox</span>
      </div>`,
    footerTemplate: `
      <div style="font-size:8px; width:100%; padding:0 12mm; color:#5c6b7a; font-family:Inter,sans-serif; display:flex; justify-content:space-between;">
        <span>Student revision booklet</span>
        <span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span>
      </div>`,
    margin: { top: "14mm", bottom: "14mm", left: "12mm", right: "12mm" },
  });
  console.log(pdfPath);
} finally {
  await browser.close();
}
