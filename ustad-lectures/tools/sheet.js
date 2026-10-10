// Renders every registered diagram whose id starts with a prefix onto one contact sheet.
// Usage: node tools/sheet.js <key e.g. xi-2> <out.png> [columns=2] [width=980]
// Renders all diagrams registered by js/diagrams/<key>.js
const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');
const web = path.join(__dirname, '../app/src/main/assets/web');
const [key = '', out = '/tmp/sheet.png', cols = '2', width = '980'] = process.argv.slice(2);
(async () => {
  const files = [key + '.js'];
  const scripts = ['core.js', 'kit.js'].map((f) => fs.readFileSync(path.join(web, 'js', f), 'utf8'))
    .concat(files.map((f) => fs.readFileSync(path.join(web, 'js/diagrams', f), 'utf8')));
  const css = fs.readFileSync(path.join(web, 'css/app.css'), 'utf8')
    .replace(/url\('\.\.\/fonts\/([^']+)'\)/g, (m, f) => "url('file://" + path.join(web, 'fonts', f) + "')");
  const html = `<!doctype html><html data-theme="${process.env.THEME || 'light'}"><head><meta charset="utf-8"><style>${css}
   body{height:auto;padding:12px;background:var(--bg)} .grid{display:flex;flex-wrap:wrap;gap:12px}
   .cell{flex:1 1 calc(${100 / +cols}% - 12px);min-width:0;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:8px;display:flex;flex-direction:column;align-items:center}
   .cell small{color:var(--mut);font:12px monospace;align-self:flex-start}</style></head><body><div class="grid" id="g"></div>
   <script>${scripts.join('\n;\n')}</script>
   <script>const ids=Object.keys(Diagrams.reg);
   document.getElementById('g').innerHTML=ids.map(i=>'<div class="cell"><small>'+i+'</small>'+Diagrams.render(i,{})+'</div>').join('');
   document.title=ids.length;</script></body></html>`;
  const f = '/tmp/sheet_' + process.pid + '.html';
  fs.writeFileSync(f, html);
  const b = await puppeteer.launch({ executablePath: '/opt/google/chrome/chrome', args: ['--no-sandbox', '--allow-file-access-from-files'], headless: 'new' });
  const p = await b.newPage();
  const logs = [];
  p.on('pageerror', (e) => logs.push('PAGEERROR ' + e.message));
  await p.setViewport({ width: +width, height: 600, deviceScaleFactor: 1.5 });
  await p.goto('file://' + f);
  await new Promise((r) => setTimeout(r, 800));
  console.log('diagrams rendered: ' + (await p.title()));
  await p.screenshot({ path: out, fullPage: true });
  console.log(logs.join('\n'));
  await b.close();
  fs.unlinkSync(f);
})();
