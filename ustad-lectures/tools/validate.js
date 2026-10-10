#!/usr/bin/env node
/* Validates lecture data + diagrams.
 *   node tools/validate.js            -> every data file
 *   node tools/validate.js xi-2 xi-3  -> only those keys (data/<key>.js, diagrams/<key>.js)
 * Exit code 1 when there are errors. Warnings do not fail the run.
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const web = path.join(__dirname, '../app/src/main/assets/web/js');
const keysArg = process.argv.slice(2);
const allKeys = fs
  .readdirSync(path.join(web, 'data'))
  .filter((f) => f.endsWith('.js'))
  .map((f) => f.replace(/\.js$/, ''))
  .sort();
const keys = keysArg.length ? keysArg : allKeys;

const ctx = { console };
ctx.window = ctx;
ctx.globalThis = ctx;
vm.createContext(ctx);
const load = (f) => vm.runInContext(fs.readFileSync(f, 'utf8'), ctx, { filename: f });
['core.js', 'kit.js', 'speech.js'].forEach((f) => load(path.join(web, f)));
new Set(keys.map((k) => k.replace(/-p\d$/, ''))).forEach((k) => {
  const f = path.join(web, 'diagrams', k + '.js');
  if (fs.existsSync(f)) load(f);
});
const before = new Set();
keys.forEach((k) => {
  const f = path.join(web, 'data', k + '.js');
  if (!fs.existsSync(f)) {
    console.error('missing data file ' + f);
    process.exit(1);
  }
  const n0 = ctx.Lectures.list.length;
  load(f);
});

const errors = [];
const warns = [];
const err = (id, m) => errors.push(id + ': ' + m);
const warn = (id, m) => warns.push(id + ': ' + m);

const AR = /[\u0600-\u06FF]/g;
const LAT = /[A-Za-z]/g;
const BLOCKS = new Set(['h', 'say', 'points', 'recap', 'math', 'diagram', 'svg', 'dgrow', 'table', 'compare', 'terms', 'steps', 'code', 'note']);
const NEEDS_SAY = new Set(['diagram', 'svg', 'dgrow', 'table', 'compare', 'code']);
const NOTE_KINDS = new Set(['tip', 'warn', 'exam', 'example', 'def']);
const texList = [];

function strs(b) {
  const out = [];
  const walk = (v) => {
    if (typeof v === 'string') out.push(v);
    else if (Array.isArray(v)) v.forEach(walk);
    else if (v && typeof v === 'object') Object.keys(v).forEach((k) => (k === 'args' || k === 'svg' ? 0 : walk(v[k])));
  };
  walk(b);
  return out;
}

const mine = ctx.Lectures.list.filter((l) => keys.some((k) => l.id && l.__file === undefined));
const wanted = ctx.Lectures.list;
const seen = new Set();
let totalWords = 0;
let totalUnits = 0;

wanted.forEach((l) => {
  const id = l.id || '(no id)';
  if (seen.has(id)) err(id, 'duplicate lecture id');
  seen.add(id);
  const m = /^(xi|xii)-(\d)-(\d\d)$/.exec(l.id || '');
  if (!m) return err(id, 'id must look like xi-1-01 / xii-3-02');
  if (l.cls !== m[1].toUpperCase()) err(id, 'cls does not match id');
  if (l.ch !== +m[2]) err(id, 'ch does not match id');
  if (l.n !== +m[3]) err(id, 'n must equal the number in the id');
  if (!l.title || !/[A-Za-z]/.test(l.title)) err(id, 'title (English) required');
  if (!l.titleUr || !AR.test(l.titleUr)) err(id, 'titleUr must be Urdu script');
  AR.lastIndex = 0;
  if (!l.source) warn(id, 'source missing (e.g. "Unit 1 · §1.1.4")');
  if (!(l.mins >= 4 && l.mins <= 20)) warn(id, 'mins should be 4..20');
  if (!Array.isArray(l.objectives) || l.objectives.length < 2) err(id, 'need >= 2 objectives');
  if (!Array.isArray(l.blocks) || l.blocks.length < 8) err(id, 'need >= 8 blocks');
  if (!Array.isArray(l.quiz) || l.quiz.length < 3) err(id, 'need >= 3 quiz questions');
  if (!Array.isArray(l.homework) || l.homework.length < 1) err(id, 'need homework');
  (l.quiz || []).forEach((q, i) => {
    if (!q.q || !Array.isArray(q.opts) || q.opts.length < 2 || q.opts.length > 5) err(id, 'quiz ' + i + ' malformed');
    else if (!(q.a >= 0 && q.a < q.opts.length)) err(id, 'quiz ' + i + ' answer index out of range');
    if (!q.why) err(id, 'quiz ' + i + ' needs why');
    strs(q).forEach((s) => collectTex(id, s));
  });
  strs({ o: l.objectives, h: l.homework }).forEach((s) => collectTex(id, s));

  let words = 0;
  let units = 0;
  let diagrams = 0;
  let maths = 0;
  let codes = 0;
  const types = {};
  (l.blocks || []).forEach((b, i) => {
    const at = id + ' block#' + i + ' (' + b.t + ')';
    if (!BLOCKS.has(b.t)) return err(at, 'unknown block type');
    types[b.t] = (types[b.t] || 0) + 1;
    if (NEEDS_SAY.has(b.t) && !b.say) err(at, 'needs `say` narration');
    if (b.t === 'diagram') {
      diagrams++;
      if (!ctx.Diagrams.has(b.id)) err(at, 'unknown diagram id ' + b.id);
      else checkSvg(at, ctx.Diagrams.render(b.id, b.args));
    }
    if (b.t === 'svg') {
      diagrams++;
      checkSvg(at, b.svg || '');
    }
    if (b.t === 'dgrow') {
      (b.items || []).forEach((it) => {
        diagrams++;
        if (it.svg) checkSvg(at, it.svg);
        else if (!ctx.Diagrams.has(it.id)) err(at, 'unknown diagram id ' + it.id);
        else checkSvg(at, ctx.Diagrams.render(it.id, it.args));
      });
    }
    if (b.t === 'math') {
      maths++;
      if (!b.tex) err(at, 'math needs tex');
      else texList.push({ at, tex: b.tex, display: true });
    }
    if (b.t === 'code') {
      codes++;
      if (!b.code) err(at, 'code needs code');
    }
    if (b.t === 'note' && !NOTE_KINDS.has(b.kind || 'tip')) err(at, 'bad note kind');
    if (b.t === 'table' && (!b.rows || !b.rows.length)) err(at, 'table needs rows');
    if (b.t === 'compare' && !(b.left && b.right)) err(at, 'compare needs left & right');
    if (['say', 'h', 'note'].includes(b.t) && !b.ur) err(at, 'needs `ur` text');
    if (['points', 'recap', 'steps'].includes(b.t) && !(b.items && b.items.length)) err(at, 'needs items');
    if (b.t === 'terms' && !(b.items && b.items.length && b.items.every((t) => t.en && t.ur))) err(at, 'terms need {en, ur}');

    strs(b).forEach((s) => collectTex(at, s));
    // narration text for this block
    const spoken = [];
    if (b.ur) spoken.push(b.ur);
    if (b.say) spoken.push(b.say);
    if (b.t === 'points' || b.t === 'recap' || b.t === 'steps') spoken.push((b.title || '') + ' ' + (b.items || []).join(' '));
    if (b.t === 'terms') spoken.push((b.items || []).map((t) => t.en + ' ' + t.ur).join(' '));
    const sp = spoken.join(' ');
    words += (sp.match(/\S+/g) || []).length;
    units += ctx.Speech.splitSentences(sp).length;
    if (sp && (b.t === 'say' || b.t === 'h' || b.t === 'note' || b.say)) {
      const ar = (sp.match(AR) || []).length;
      const la = (sp.replace(/\$[^$]*\$/g, '').match(LAT) || []).length;
      if (b.t !== 'h' && ar < 8) err(at, 'narration must be Urdu script (Urdish): found almost no Urdu letters');
      if (ar > 0 && la / (ar + la) > 0.65 && b.t === 'say') warn(at, 'too much English; keep Urdu descriptive, English terminology only');
    }
    spoken.forEach((s) => {
      if (/\$[^$]*$/.test(s.replace(/\$[^$]*\$/g, ''))) err(at, 'unbalanced $ in text');
      if (/[A-Za-z]{3,}.*\d/.test('') ) return;
    });
  });
  totalWords += words;
  totalUnits += units;
  if (words < 450) warn(id, 'narration only ~' + words + ' words (aim 700-1400 => 6-12 min)');
  if (diagrams < 1) warn(id, 'no diagram in this lecture');
  console.log(
    id.padEnd(10) + ' ' + String(l.title).slice(0, 44).padEnd(44) + ' blocks=' + String(l.blocks.length).padStart(2) + ' words=' + String(words).padStart(4) +
      ' dg=' + diagrams + ' math=' + maths + ' code=' + codes + ' quiz=' + (l.quiz || []).length
  );
});

function collectTex(at, s) {
  if (typeof s !== 'string') return;
  s.replace(/\$([^$]+)\$/g, (m, t) => {
    texList.push({ at, tex: t, display: false });
    return m;
  });
}

function checkSvg(at, s) {
  if (!/^<svg[\s>]/.test(s.trim())) return err(at, 'diagram did not produce <svg>: ' + s.slice(0, 80));
  if (/NaN|undefined|Infinity/.test(s)) err(at, 'diagram svg contains NaN/undefined');
  const m = /viewBox="0 0 (\d+(?:\.\d+)?) (\d+(?:\.\d+)?)"/.exec(s);
  if (!m) err(at, 'diagram missing viewBox');
  else if (+m[1] > 520) warn(at, 'diagram width ' + m[1] + ' > 520: text will be tiny on phones');
  if ((s.match(/<svg/g) || []).length !== 1) err(at, 'diagram must contain exactly one <svg>');
}

(async () => {
  try {
    const MJ = await require('mathjax').init({ loader: { load: ['input/tex', 'output/svg'] }, tex: { macros: { XOR: '\\oplus', NOT: ['\\overline{#1}', 1] } } });
    texList.forEach(({ at, tex, display }) => {
      let out = '';
      try {
        out = MJ.startup.adaptor.outerHTML(MJ.tex2svg(tex, { display }));
      } catch (e) {
        return err(at, 'TeX error: ' + e.message + ' in: ' + tex);
      }
      if (/data-mml-node="merror"/.test(out)) {
        const t = /<title[^>]*>([^<]*)/.exec(out);
        err(at, 'TeX error: ' + (t ? t[1] : 'merror') + ' in: ' + tex);
      }
    });
  } catch (e) {
    warn('tools', 'MathJax node check skipped: ' + e.message + ' (run: cd tools && npm install)');
  }
  console.log('\n' + wanted.length + ' lectures, ~' + totalWords + ' narrated words, ' + totalUnits + ' speech units, ' + texList.length + ' TeX snippets checked');
  warns.forEach((w) => console.log('WARN  ' + w));
  errors.forEach((e) => console.log('ERROR ' + e));
  console.log(errors.length ? '\nFAILED: ' + errors.length + ' error(s)' : '\nOK');
  process.exit(errors.length ? 1 : 0);
})();
