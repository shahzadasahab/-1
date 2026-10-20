import puppeteer from 'puppeteer-core';
import { pathToFileURL } from 'url';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const htmlPath = join(__dirname, 'chapter-1-lecture-notes.html');
const pdfPath = join(__dirname, 'Chapter-1-Computer-Systems-Lecture-Notes.pdf');
const chrome = process.env.CHROME_PATH || '/usr/local/bin/google-chrome';

const browser = await puppeteer.launch({
  executablePath: chrome,
  headless: true,
  args: ['--no-sandbox', '--disable-setuid-sandbox', '--font-render-hinting=none'],
});

const page = await browser.newPage();
await page.goto(pathToFileURL(htmlPath).href, { waitUntil: 'networkidle0', timeout: 120000 });

await page.waitForFunction(() => {
  return window.MathJax?.startup?.promise?.then
    ? window.MathJax.startup.promise.then(() => true)
    : document.querySelector('mjx-container') !== null;
}, { timeout: 60000 }).catch(() => {
  console.warn('MathJax wait timed out; continuing with PDF export.');
});

await page.pdf({
  path: pdfPath,
  format: 'A4',
  printBackground: true,
  margin: { top: '12mm', right: '10mm', bottom: '14mm', left: '10mm' },
});

await browser.close();
console.log('Wrote', pdfPath);
