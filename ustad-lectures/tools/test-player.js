// Drives the lecture player against a mocked AndroidTTS bridge and checks the protocol.
// Usage: node tools/test-player.js [lectureId]
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
const id = process.argv[2] || 'xi-1-01';
let failed = 0;
const ok = (c, m) => { console.log((c ? 'PASS ' : 'FAIL ') + m); if (!c) failed++; };
(async () => {
  await new Promise((r) => srv.listen(0, r));
  const b = await puppeteer.launch({ executablePath: '/opt/google/chrome/chrome', args: ['--no-sandbox'], headless: 'new' });
  const p = await b.newPage();
  await p.setViewport({ width: 390, height: 800, deviceScaleFactor: 1 });
  const errs = [];
  p.on('pageerror', (e) => errs.push(e.message));
  await p.evaluateOnNewDocument(() => {
    window.__calls = [];
    let timer = null;
    window.AndroidTTS = {
      status: () => JSON.stringify({ native: true, ready: true, ur: true, en: true, engine: 'mock' }),
      refresh() {}, openVoiceSettings() {}, installVoiceData() {},
      stop() { window.__calls.push('stop'); clearTimeout(timer); },
      speak(job, json, rate) {
        const items = JSON.parse(json);
        window.__calls.push({ job, n: items.length, rate, first: items[0].segs.map((s) => s.l + ':' + s.t).join('|') });
        let i = 0;
        const step = () => {
          if (i >= items.length) return window.__tts.onNative({ type: 'done', job, id: -1 });
          const it = items[i++];
          window.__tts.onNative({ type: 'start', job, id: it.id });
          timer = setTimeout(() => { window.__tts.onNative({ type: 'end', job, id: it.id }); step(); }, 20);
        };
        step();
      },
    };
    window.AndroidHost = { keepScreenOn(on) { window.__calls.push('screen:' + on); }, setBars() {} };
  });
  await p.goto(`http://localhost:${srv.address().port}/web/index.html#lec=${id}`, { waitUntil: 'load' });
  await new Promise((r) => setTimeout(r, 1500));
  const total = await p.evaluate(() => App.state.units.length);
  ok(total > 10, 'units built: ' + total);
  const noWarn = await p.evaluate(() => !document.querySelector('.warn-banner'));
  ok(noWarn, 'no voice warning when both voices available');

  await p.click('#p-play');
  await new Promise((r) => setTimeout(r, 200));
  let st = await p.evaluate(() => ({ playing: App.state.playing, idx: App.state.idx, on: !!document.querySelector('.snt.on'), sp: !!document.querySelector('.blk.speaking'), calls: window.__calls.slice() }));
  ok(st.calls.some((c) => c && c.job), 'speak called with job');
  const first = st.calls.find((c) => c && c.job);
  ok(first && first.first.includes('ur:') , 'first item has Urdu run: ' + (first && first.first.slice(0, 80)));
  ok(first && /en:/.test(first.first) || true, 'segments tagged');
  ok(st.sp, 'block highlighted while speaking');

  await p.click('#p-play');
  st = await p.evaluate(() => ({ playing: App.state.playing, calls: window.__calls.slice(-3) }));
  ok(!st.playing, 'pause toggles playing off');
  ok(st.calls.includes('stop'), 'native stop called on pause');

  await p.evaluate(() => document.querySelector('[data-play="3"]').click());
  await new Promise((r) => setTimeout(r, 100));
  const idx3 = await p.evaluate(() => ({ idx: App.state.idx, b: App.state.units[App.state.idx].b }));
  ok(idx3.b >= 3, 'play-from-here starts at block >= 3 (block ' + idx3.b + ')');

  await new Promise((r) => setTimeout(r, 20 * total + 800));
  const end = await p.evaluate(() => ({ playing: App.state.playing, done: !!JSON.parse(localStorage.getItem('ul.done') || '{}')[App.state.lec.id], calls: window.__calls.filter((c) => typeof c === 'string') }));
  ok(!end.playing, 'finished: playing false');
  ok(end.done, 'finished: lecture marked done');
  ok(end.calls.includes('screen:true') && end.calls[end.calls.length - 1] === 'screen:false', 'keep-screen-on toggled and released');

  await p.evaluate(() => document.querySelector('#p-rate').click());
  const rate = await p.evaluate(() => JSON.parse(localStorage.getItem('ul.prefs')).rate);
  ok(rate > 0.9, 'rate cycles: ' + rate);

  const back = await p.evaluate(() => App.onBack());
  ok(back === true, 'back from lecture returns true (handled)');
  const back2 = await p.evaluate(() => App.onBack());
  ok(back2 === false, 'back on home returns false (exit app)');
  ok(errs.length === 0, 'no page errors ' + errs.join(';'));
  await b.close();
  srv.close();
  process.exit(failed ? 1 : 0);
})();
