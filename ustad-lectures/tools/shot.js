// Usage: NODE_PATH=/tmp/pt/node_modules node tools/shot.js "<hash>" out.png [width] [height] [fullscroll]
const puppeteer = require('puppeteer-core');
const http = require('http');
const fs = require('fs');
const path = require('path');
const root = path.join(__dirname, '../app/src/main/assets');
const mime = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.ttf': 'font/ttf' };
const srv = http.createServer((q, r) => {
  const f = path.join(root, decodeURIComponent(q.url.split('?')[0]));
  if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) { r.writeHead(404); return r.end(); }
  r.writeHead(200, { 'content-type': mime[path.extname(f)] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(r);
});
(async () => {
  await new Promise((res) => srv.listen(0, res));
  const port = srv.address().port;
  const [hash, out, w = 390, h = 800, mode = ''] = process.argv.slice(2);
  const b = await puppeteer.launch({ executablePath: '/opt/google/chrome/chrome', args: ['--no-sandbox', '--force-color-profile=srgb'], headless: 'new' });
  const p = await b.newPage();
  await p.setViewport({ width: +w, height: +h, deviceScaleFactor: 2 });
  const logs = [];
  p.on('console', (m) => logs.push(m.type() + ': ' + m.text()));
  p.on('response', (r) => { if (r.status() >= 400) logs.push('HTTP ' + r.status() + ' ' + r.url()); });
  p.on('pageerror', (e) => logs.push('PAGEERROR: ' + e.message));
  await p.goto(`http://localhost:${port}/web/index.html${hash}`, { waitUntil: 'load' });
  await new Promise((r) => setTimeout(r, 2500));
  if (mode === 'full') {
    const sel = '#lec-scroll';
    const hgt = await p.evaluate((s) => { const e = document.querySelector(s) || document.scrollingElement; return e.scrollHeight; }, sel);
    await p.setViewport({ width: +w, height: Math.min(hgt + 160, 16000), deviceScaleFactor: 2 });
    await new Promise((r) => setTimeout(r, 1200));
  }
  if (/^scroll:/.test(mode)) {
    const y = +mode.split(':')[1];
    await p.evaluate((y) => { const e = document.querySelector('#lec-scroll') || document.querySelector('#home-scroll'); if (e) e.scrollTop = y; }, y);
    await new Promise((r) => setTimeout(r, 400));
  }
  await p.screenshot({ path: out });
  console.log(logs.join('\n'));
  await b.close();
  srv.close();
})();
