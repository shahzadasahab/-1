import puppeteer from "puppeteer-core";

const htmlPath = "file:///workspace/lecture-notes/class-xi-computer-science.html";
const pdfPath = "/workspace/lecture-notes/Class-XI-Computer-Science-Lecture-Notes.pdf";

const browser = await puppeteer.launch({
  executablePath: "/usr/bin/google-chrome",
  headless: true,
  args: ["--no-sandbox", "--disable-gpu", "--font-render-hinting=none"],
});

try {
  const page = await browser.newPage();
  page.setDefaultTimeout(120000);
  await page.goto(htmlPath, { waitUntil: "networkidle0", timeout: 120000 });
  await page.waitForFunction(
    () => document.documentElement.getAttribute("data-mathjax") === "ready",
    { timeout: 120000 }
  );
  await page.pdf({
    path: pdfPath,
    format: "A4",
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: `
      <div style="font-family: Inter, Liberation Sans, sans-serif; font-size: 8px; width: 100%; padding: 0 12mm; color: #4c5870; display: flex; justify-content: space-between;">
        <span>Class XI Computer Science</span>
        <span>Lecture Notes</span>
      </div>`,
    footerTemplate: `
      <div style="font-family: Inter, Liberation Sans, sans-serif; font-size: 8px; width: 100%; padding: 0 12mm; color: #4c5870; display: flex; justify-content: space-between;">
        <span>Units 1–6 · original lecture notes</span>
        <span><span class="pageNumber"></span> / <span class="totalPages"></span></span>
      </div>`,
    margin: { top: "14mm", bottom: "12mm", left: "12mm", right: "12mm" },
  });
  console.log(pdfPath);
} finally {
  await browser.close();
}
