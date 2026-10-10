/* Ustad Lectures - UI: home, lecture renderer, narration player, quiz, settings. */
(function (g) {
  'use strict';

  const $ = (s, r) => (r || document).querySelector(s);
  const $$ = (s, r) => Array.from((r || document).querySelectorAll(s));
  const esc = U.esc;
  const inline = U.inline;

  /* ---------- persistence ---------- */
  const store = {
    get(k, d) {
      try {
        const v = localStorage.getItem('ul.' + k);
        return v == null ? d : JSON.parse(v);
      } catch (e) {
        return d;
      }
    },
    set(k, v) {
      try {
        localStorage.setItem('ul.' + k, JSON.stringify(v));
      } catch (e) {}
    },
  };
  const prefs = Object.assign({ font: 'naskh', size: 1, rate: 0.9, theme: 'auto', cls: 'XI' }, store.get('prefs', {}));
  const done = store.get('done', {});
  const savePrefs = () => store.set('prefs', prefs);

  /* ---------- icons ---------- */
  const I = {
    back: '<svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg>',
    gear: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/></svg>',
    chev: '<svg class="chev" viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></svg>',
    play: '<svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>',
    pause: '<svg viewBox="0 0 24 24"><path d="M6 5h4v14H6zM14 5h4v14h-4z"/></svg>',
    prev: '<svg viewBox="0 0 24 24"><path d="M6 6h2v12H6zM9.5 12l8.5 6V6z"/></svg>',
    next: '<svg viewBox="0 0 24 24"><path d="M16 6h2v12h-2zM6 18l8.5-6L6 6z"/></svg>',
    spk: '<svg viewBox="0 0 24 24"><path d="M3 9v6h4l5 4V5L7 9z"/><path d="M16 8a5 5 0 0 1 0 8M19 5a9 9 0 0 1 0 14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    search:
      '<svg viewBox="0 0 24 24" style="width:20px;height:20px;fill:none;stroke:var(--mut);stroke-width:2;stroke-linecap:round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>',
  };

  const app = $('#app');
  let view = 'home';
  let sheetOpen = false;
  let toastTimer = 0;

  function toast(msg) {
    const t = $('#toast');
    t.textContent = msg;
    t.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => t.classList.remove('show'), 2800);
  }

  function applyPrefs() {
    const root = document.documentElement;
    const dark = prefs.theme === 'dark' || (prefs.theme === 'auto' && g.matchMedia && g.matchMedia('(prefers-color-scheme: dark)').matches);
    root.dataset.theme = dark ? 'dark' : 'light';
    root.dataset.font = prefs.font;
    root.style.setProperty('--scale', prefs.size);
    if (g.AndroidHost) {
      try {
        g.AndroidHost.setBars(dark ? '#0d1513' : '#0f766e', dark);
      } catch (e) {}
    }
  }

  function markDone(id) {
    if (!done[id]) {
      done[id] = Date.now();
      store.set('done', done);
    }
  }

  /* =====================================================================
   *  HOME
   * ===================================================================== */
  let query = '';
  const openCh = store.get('openCh', {});

  function renderHome() {
    view = 'home';
    stopSpeech();
    const all = Lectures.sorted();
    const doneCount = all.filter((l) => done[l.id]).length;
    const last = store.get('last', null);
    const lastLec = last && Lectures.byId(last.id);
    const pct = all.length ? Math.round((doneCount / all.length) * 100) : 0;

    app.innerHTML =
      '<header class="topbar"><h1>Ustad Lectures<span class="sub">Computer Science XI &amp; XII &middot; Urdish lectures with voice</span></h1>' +
      '<button class="icon-btn" id="btn-set" aria-label="Settings">' + I.gear + '</button></header>' +
      '<main class="scroll" id="home-scroll">' +
      '<section class="hero"><p class="ur-title">' + inline('السلام علیکم! آج کا **Lecture** منتخب کریں') + '</p>' +
      '<p>Teacher-style lectures: Urdu explanation, English terminology, MathJax formulas and SVG diagrams, read aloud with TTS.</p>' +
      '<div class="row"><div class="stat"><b>' + all.length + '</b>Lectures</div><div class="stat"><b>' + doneCount + '</b>Completed</div>' +
      '<div class="stat"><b>' + Chapters.length + '</b>Chapters</div>' +
      (lastLec
        ? '<button class="btn light" id="btn-cont" style="margin-left:auto">Continue &rsaquo;</button>'
        : '<button class="btn light" id="btn-start" style="margin-left:auto">Start Lecture 1 &rsaquo;</button>') +
      '<div class="bar"><i style="width:' + pct + '%"></i></div></div></section>' +
      '<div class="tabs"><button class="tab' + (prefs.cls === 'XI' ? ' on' : '') + '" data-cls="XI">Class XI<small>First Year</small></button>' +
      '<button class="tab' + (prefs.cls === 'XII' ? ' on' : '') + '" data-cls="XII">Class XII<small>Second Year</small></button></div>' +
      '<label class="search">' + I.search + '<input id="q" type="search" placeholder="Search lectures (e.g. gate, SDLC, loop)" value="' + esc(query) + '"></label>' +
      '<div id="chapters" style="display:flex;flex-direction:column;gap:12px"></div>' +
      '<p class="foot-note">Tap the speaker button inside any lecture to hear the teacher. Install an Urdu TTS voice for best results.</p>' +
      '</main>';

    $('#btn-set').onclick = openSettings;
    const c = $('#btn-cont');
    if (c) c.onclick = () => openLecture(last.id, last.u || 0);
    const s = $('#btn-start');
    if (s && all.length) s.onclick = () => openLecture(all.filter((l) => l.cls === prefs.cls)[0].id);
    $$('.tab').forEach((t) => {
      t.onclick = () => {
        prefs.cls = t.dataset.cls;
        savePrefs();
        $$('.tab').forEach((x) => x.classList.toggle('on', x === t));
        renderChapters();
      };
    });
    $('#q').oninput = (e) => {
      query = e.target.value.trim().toLowerCase();
      renderChapters();
    };
    renderChapters();
    typeset($('#home-scroll'));
  }

  function renderChapters() {
    const host = $('#chapters');
    if (!host) return;
    let html = '';
    Chapters.filter((c) => c.cls === prefs.cls).forEach((c) => {
      const all = Lectures.forChapter(c.cls, c.ch);
      let lecs = all;
      if (query) {
        lecs = all.filter((l) =>
          (l.title + ' ' + (l.titleUr || '') + ' ' + c.en + ' ' + (l.source || '') + ' ' + (l.keywords || []).join(' ')).toLowerCase().includes(query)
        );
        if (!lecs.length) return;
      }
      const dn = all.filter((l) => done[l.id]).length;
      const open = query ? true : !!openCh[c.cls + c.ch];
      html +=
        '<section class="chapter' + (open ? ' open' : '') + '" data-k="' + c.cls + c.ch + '">' +
        '<button class="chapter-head"><span class="badge" style="background:var(--chip' + c.color + ')">' + c.ch + '</span>' +
        '<span class="ch-text"><b>' + esc(c.en) + '</b><span class="ur">' + esc(c.ur) + '</span><small>' + esc(c.sub) + '</small></span>' +
        '<span class="ch-meta"><b>' + dn + '/' + all.length + '</b>lectures</span>' + I.chev + '</button>' +
        '<div class="lec-list">' +
        (lecs.length
          ? lecs
              .map(
                (l, i) =>
                  '<button class="lec-row' + (done[l.id] ? ' done' : '') + '" data-id="' + l.id + '"><span class="lec-no">' +
                  (done[l.id] ? '&#10003;' : 'L' + (l.n || i + 1)) + '</span><span class="lec-t"><b>' + esc(l.title) + '</b><span class="ur">' +
                  esc(l.titleUr || '') + '</span></span><span class="lec-min">' + (l.mins || 8) + ' min</span></button>'
              )
              .join('')
          : '<div class="empty">Lectures for this chapter are coming soon.</div>') +
        '</div></section>';
    });
    host.innerHTML = html || '<div class="empty">No lectures match your search.</div>';
    $$('.chapter-head', host).forEach((b) => {
      b.onclick = () => {
        const sec = b.parentElement;
        sec.classList.toggle('open');
        openCh[sec.dataset.k] = sec.classList.contains('open');
        store.set('openCh', openCh);
      };
    });
    $$('.lec-row', host).forEach((b) => {
      b.onclick = () => openLecture(b.dataset.id);
    });
  }

  /* =====================================================================
   *  LECTURE RENDERING
   * ===================================================================== */
  const P = { lec: null, units: [], idx: 0, playing: false, job: 0, blockFirst: [], missingShown: false };
  const LABELS = { tip: 'ٹپ', warn: 'خبردار', exam: 'امتحان', example: 'مثال', def: 'تعریف' };

  function highlightCode(src, lang) {
    const kw = new Set(
      'def return if elif else for while in not and or import from as class try except finally with pass break continue True False None lambda global nonlocal is del raise yield assert'.split(' ')
    );
    const bi = new Set('print input len range int float str list dict set tuple open sum min max sorted bool abs round type enumerate zip map filter append sort'.split(' '));
    const sql = new Set(
      'SELECT FROM WHERE INSERT INTO VALUES CREATE TABLE PRIMARY KEY UPDATE SET DELETE ORDER BY GROUP AND OR NOT NULL INTEGER TEXT REAL JOIN ON AS COUNT AVG SUM MAX MIN LIKE DISTINCT HAVING LIMIT ASC DESC FOREIGN REFERENCES IN BETWEEN'.split(' ')
    );
    const isSql = /sql/i.test(lang || '');
    const re = /(#[^\n]*|--[^\n]*)|("""[\s\S]*?"""|'''[\s\S]*?'''|"(?:\\.|[^"\\\n])*"|'(?:\\.|[^'\\\n])*')|(\b\d+(?:\.\d+)?\b)|([A-Za-z_][A-Za-z0-9_]*)/g;
    let out = '';
    let last = 0;
    src.replace(re, (m, com, str, num, id, off) => {
      out += esc(src.slice(last, off));
      last = off + m.length;
      if (com && (!isSql ? m[0] === '#' : m[0] === '-' || m[0] === '#')) out += '<span class="c">' + esc(m) + '</span>';
      else if (com) out += esc(m);
      else if (str) out += '<span class="s">' + esc(m) + '</span>';
      else if (num) out += '<span class="n">' + esc(m) + '</span>';
      else if (id) {
        if (isSql ? sql.has(id.toUpperCase()) : kw.has(id)) out += '<span class="k">' + esc(m) + '</span>';
        else if (!isSql && bi.has(id)) out += '<span class="f">' + esc(m) + '</span>';
        else out += esc(m);
      } else out += esc(m);
      return m;
    });
    return out + esc(src.slice(last));
  }

  function figure(b) {
    const inner = b.svg ? b.svg : Diagrams.render(b.id, b.args);
    return '<figure class="fig"><div class="fig-svg">' + inner + '</div>' + (b.cap ? '<figcaption class="cap">' + inline(b.cap) + '</figcaption>' : '') + '</figure>';
  }

  /** Builds block HTML while collecting the narration units that go with it. */
  function buildLecture(lec) {
    const units = [];
    let bi = 0;

    /* text with sentence spans: each sentence is one narration unit */
    const sent = (text) =>
      Speech.splitSentences(text)
        .map((s) => {
          const id = units.length;
          units.push({ b: bi, text: s });
          return '<span class="snt" data-u="' + id + '">' + inline(s) + '</span>';
        })
        .join(' ');
    /* narration without a text node to highlight (diagram, table, code ...) */
    const say = (text) => {
      if (text) Speech.splitSentences(text).forEach((s) => units.push({ b: bi, text: s }));
    };
    /* a single unit attached to a chip-like element */
    const one = (text) => {
      const id = units.length;
      units.push({ b: bi, text });
      return id;
    };
    const wrap = (cls, inner) =>
      '<div class="blk ' + cls + '" data-b="' + bi + '"><button class="blk-play" data-play="' + bi + '" aria-label="Play from here">' + I.play + '</button>' + inner + '</div>';

    const html = (lec.blocks || []).map((b, i) => {
      bi = i;
      switch (b.t) {
        case 'h':
          return wrap('blk-h', '<h3 class="rtl">' + sent(b.ur) + '</h3>');
        case 'say':
          return wrap('say-b', '<p class="rtl say">' + sent(b.ur) + '</p>');
        case 'points':
        case 'recap': {
          const tag = b.ordered ? 'ol' : 'ul';
          const ttl = b.title || (b.t === 'recap' ? 'بورڈ سمری (Board Summary)' : '');
          const head = ttl ? '<p class="rtl ttl">' + sent(ttl) + '</p>' : '';
          const items = (b.items || []).map((it) => '<li>' + sent(it) + '</li>').join('');
          return wrap('pts' + (b.t === 'recap' ? ' recap' : ''), head + '<' + tag + ' class="rtl">' + items + '</' + tag + '>');
        }
        case 'math':
          say(b.say || Speech.texToSpeech(b.tex));
          return wrap('math', '<div class="tex">\\[' + esc(b.tex) + '\\]</div>' + (b.cap ? '<p class="cap">' + inline(b.cap) + '</p>' : ''));
        case 'diagram':
        case 'svg':
          say(b.say);
          return wrap('fig-b', figure(b));
        case 'dgrow':
          say(b.say);
          return wrap('fig-b', '<div class="dgrow">' + (b.items || []).map(figure).join('') + '</div>');
        case 'table': {
          say(b.say);
          const cell = (c) => '<div class="td"><span class="tc">' + inline(c) + '</span></div>';
          const head = b.head ? '<div class="tr th">' + b.head.map(cell).join('') + '</div>' : '';
          const rows = (b.rows || []).map((r) => '<div class="tr">' + r.map(cell).join('') + '</div>').join('');
          return wrap('tbl-b', (b.title ? '<p class="cap" style="text-align:start">' + inline(b.title) + '</p>' : '') + '<div class="tbl-wrap"><div class="tbl" role="table">' + head + rows + '</div></div>');
        }
        case 'compare': {
          say(b.say);
          const side = (s) => '<div class="side"><p class="ttl">' + inline(s.title) + '</p><ul>' + (s.items || []).map((x) => '<li>' + inline(x) + '</li>').join('') + '</ul></div>';
          return wrap('cmp', '<div class="compare">' + side(b.left) + side(b.right) + '</div>');
        }
        case 'terms': {
          const chips = (b.items || [])
            .map((t) => {
              const id = one('**' + t.en + '** یعنی ' + t.ur);
              return '<div class="term snt" data-u="' + id + '"><b>' + esc(t.en) + '</b><span>' + inline(t.ur) + '</span></div>';
            })
            .join('');
          return wrap('terms-b', '<div class="terms">' + chips + '</div>');
        }
        case 'steps': {
          const items = (b.items || []).map((it, k) => '<div class="step"><span class="no">' + (k + 1) + '</span><p class="rtl">' + sent(it) + '</p></div>').join('');
          return wrap('steps-b', (b.title ? '<p class="rtl ttl" style="margin:0;color:var(--brand);font-weight:700">' + sent(b.title) + '</p>' : '') + '<div class="steps">' + items + '</div>');
        }
        case 'code': {
          say(b.say);
          const out = b.out ? '<span class="out-ttl">Output</span><pre class="code out" dir="ltr"><code>' + esc(b.out) + '</code></pre>' : '';
          return wrap('code-b', '<div class="code-wrap"><span class="code-lang">' + esc(b.lang || 'python') + '</span><pre class="code" dir="ltr"><code>' + highlightCode(b.code, b.lang) + '</code></pre>' + out + '</div>');
        }
        case 'note': {
          const k = b.kind || 'tip';
          return wrap('note k-' + k, '<p class="rtl say">' + sent(b.ur) + '</p><span class="lbl">' + (LABELS[k] || LABELS.tip) + '</span>');
        }
        default:
          return '';
      }
    });
    P.units = units;
    P.blockFirst = [];
    units.forEach((u, i) => {
      if (P.blockFirst[u.b] == null) P.blockFirst[u.b] = i;
    });
    return html.join('');
  }

  function quizHtml(lec) {
    if (!lec.quiz || !lec.quiz.length) return '';
    const L = ['A', 'B', 'C', 'D', 'E'];
    return (
      '<section class="sect"><h3>Quick Quiz <span class="ur">فوری کوئز</span></h3>' +
      lec.quiz
        .map(
          (q, qi) =>
            '<div class="qz" data-qi="' + qi + '"><div class="q"><p class="rtl">' + inline(q.q) + '</p><button class="mini-btn" data-qspk="' + qi + '" aria-label="Read question">' + I.spk + '</button></div>' +
            '<div class="opts">' +
            q.opts.map((o, oi) => '<button class="opt" data-oi="' + oi + '"><span class="rtl">' + inline(o) + '</span><span class="l">' + L[oi] + '</span></button>').join('') +
            '</div><p class="rtl why">' + inline(q.why || '') + '</p></div>'
        )
        .join('') +
      '</section>'
    );
  }

  function openLecture(id, startUnit) {
    const lec = Lectures.byId(id);
    if (!lec) return;
    stopSpeech();
    view = 'lecture';
    P.lec = lec;
    P.idx = Math.max(0, startUnit || 0);
    P.playing = false;
    const ch = Chapters.find((c) => c.cls === lec.cls && c.ch === lec.ch) || {};
    const list = Lectures.forChapter(lec.cls, lec.ch);
    const all = Lectures.sorted();
    const pos = all.findIndex((l) => l.id === id);
    const prev = all[pos - 1];
    const next = all[pos + 1];
    const body = buildLecture(lec);
    if (P.idx >= P.units.length) P.idx = 0;
    store.set('last', { id, u: 0 });

    const st = Speech.status();
    const ready = !st.native || st.ready;
    const warn = ready && st.ur === false ? voiceBanner() : '';

    app.innerHTML =
      '<header class="topbar"><button class="icon-btn" id="btn-back" aria-label="Back">' + I.back + '</button>' +
      '<h1>' + esc(lec.title) + '<span class="sub">Class ' + lec.cls + ' &middot; Ch ' + lec.ch + ' &middot; ' + esc(ch.en || '') + '</span></h1>' +
      '<button class="icon-btn" id="btn-set" aria-label="Settings">' + I.gear + '</button></header>' +
      '<main class="scroll" id="lec-scroll"><article class="lecture">' +
      '<section class="lec-head"><div class="chips"><span class="chip" style="background:var(--chip' + (ch.color || 0) + ')">Class ' + lec.cls + '</span>' +
      '<span class="chip plain">Chapter ' + lec.ch + '</span><span class="chip plain">Lecture ' + (lec.n || list.findIndex((l) => l.id === id) + 1) + '</span>' +
      '<span class="chip plain">' + (lec.mins || 8) + ' min</span></div>' +
      '<h2>' + esc(lec.title) + '</h2><p class="ur-h">' + inline(lec.titleUr || '') + '</p>' +
      (lec.source ? '<span class="src">Source: ' + esc(lec.source) + '</span>' : '') +
      (lec.objectives && lec.objectives.length
        ? '<div class="pts" style="margin-top:4px"><p class="rtl ttl" style="margin:0;color:var(--brand);font-weight:700">آج کے اہداف (Objectives)</p><ul class="rtl">' +
          lec.objectives.map((o) => '<li>' + inline(o) + '</li>').join('') + '</ul></div>'
        : '') +
      '</section><div id="voice-warn">' + warn + '</div><section class="blocks" id="blocks">' + body + '</section>' +
      quizHtml(lec) +
      (lec.homework && lec.homework.length
        ? '<section class="sect hw"><h3>Homework <span class="ur">گھر کا کام</span></h3><ul>' + lec.homework.map((h) => '<li>' + inline(h) + '</li>').join('') + '</ul></section>'
        : '') +
      '<div style="display:flex;gap:10px"><button class="btn" id="btn-done" style="flex:1">Mark lecture as completed</button></div>' +
      '<nav class="lec-nav">' +
      (prev ? '<button class="btn ghost" data-go="' + prev.id + '">&lsaquo; Previous<b>' + esc(prev.title) + '</b></button>' : '<span class="btn ghost dis"></span>') +
      (next ? '<button class="btn" data-go="' + next.id + '">Next &rsaquo;<b>' + esc(next.title) + '</b></button>' : '<span class="btn dis"></span>') +
      '</nav></article></main>' +
      '<footer class="player" id="player"></footer>';

    $('#btn-back').onclick = () => renderHome();
    $('#btn-set').onclick = openSettings;
    $('#btn-done').onclick = () => {
      markDone(id);
      toast('Lecture marked as completed');
    };
    $$('[data-go]').forEach((b) => (b.onclick = () => openLecture(b.dataset.go)));
    $$('[data-play]').forEach((b) => {
      b.onclick = (e) => {
        e.stopPropagation();
        const first = P.blockFirst[+b.dataset.play];
        if (first != null) playFrom(first);
      };
    });
    bindQuiz(lec);
    renderPlayer();
    typeset($('#lec-scroll')).then(() => {
      if (startUnit) scrollToUnit(P.idx, true);
    });
    if (!ready) pollVoices();
  }

  function voiceBanner() {
    return (
      '<div class="warn-banner"><div class="col"><b>Urdu voice not installed</b>' +
      '<span>The lecture will still be shown. To hear Urdu narration, install the Urdu voice for Google Text-to-Speech (Settings &rsaquo; Text-to-speech &rsaquo; Install voice data &rsaquo; Urdu).</span>' +
      '<div class="row"><button class="btn" data-vi="install">Install Urdu voice</button><button class="btn" data-vi="settings">Voice settings</button></div></div></div>'
    );
  }

  function pollVoices() {
    let tries = 0;
    const t = setInterval(() => {
      tries++;
      const st = Speech.status();
      if ((st.ready && st.ready !== false) || tries > 20) {
        clearInterval(t);
        const w = $('#voice-warn');
        if (w && view === 'lecture') w.innerHTML = st.ready && st.ur === false ? voiceBanner() : '';
      }
    }, 600);
  }

  document.addEventListener('click', (e) => {
    const b = e.target.closest('[data-vi]');
    if (!b) return;
    if (b.dataset.vi === 'install') Speech.installVoiceData();
    else Speech.openVoiceSettings();
  });

  function bindQuiz(lec) {
    $$('.qz').forEach((box) => {
      const q = lec.quiz[+box.dataset.qi];
      $$('.opt', box).forEach((o) => {
        o.onclick = () => {
          if (box.classList.contains('answered')) return;
          box.classList.add('answered');
          const pick = +o.dataset.oi;
          $$('.opt', box).forEach((x) => {
            const i = +x.dataset.oi;
            if (i === q.a) x.classList.add('ok');
            else if (i === pick) x.classList.add('bad');
          });
          typeset(box);
        };
      });
      const sp = $('[data-qspk]', box);
      if (sp)
        sp.onclick = () => {
          pausePlayback();
          const txt = q.q + ' ' + q.opts.map((o, i) => 'Option ' + 'ABCDE'[i] + '. ' + o).join(' ');
          Speech.speak([Speech.toItem(0, txt)], prefs.rate, {});
        };
    });
  }

  /* =====================================================================
   *  PLAYER
   * ===================================================================== */
  const RATES = [0.7, 0.8, 0.9, 1.0, 1.15, 1.3];

  function renderPlayer() {
    const el = $('#player');
    if (!el) return;
    const total = P.units.length;
    const u = P.units[P.idx];
    const bTotal = (P.lec.blocks || []).length;
    el.innerHTML =
      '<button class="p-btn" id="p-prev" aria-label="Previous section">' + I.prev + '</button>' +
      '<button class="p-btn main" id="p-play" aria-label="Play or pause">' + (P.playing ? I.pause : I.play) + '</button>' +
      '<button class="p-btn" id="p-next" aria-label="Next section">' + I.next + '</button>' +
      '<div class="grow"><b>' + (P.playing ? 'Teacher is speaking...' : total ? 'Listen to this lecture' : 'No narration') + '</b>' +
      '<span>' + (total ? 'Part ' + Math.min(P.idx + 1, total) + ' of ' + total : '') + '</span></div>' +
      '<button class="p-rate" id="p-rate" aria-label="Speech speed">' + prefs.rate.toFixed(2).replace(/0$/, '') + 'x</button>';
    $('#p-play').onclick = () => (P.playing ? pausePlayback() : playFrom(P.idx));
    $('#p-prev').onclick = () => stepBlock(-1);
    $('#p-next').onclick = () => stepBlock(1);
    $('#p-rate').onclick = () => {
      let i = RATES.findIndex((r) => Math.abs(r - prefs.rate) < 0.01);
      i = (i + 1) % RATES.length;
      prefs.rate = RATES[i];
      savePrefs();
      renderPlayer();
      if (P.playing) playFrom(P.idx);
    };
  }

  function stepBlock(dir) {
    if (!P.units.length) return;
    const cur = P.units[Math.min(P.idx, P.units.length - 1)].b;
    let target = null;
    if (dir > 0) {
      for (let i = P.idx; i < P.units.length; i++) if (P.units[i].b > cur) { target = i; break; }
    } else {
      const firstOfCur = P.blockFirst[cur];
      const start = P.idx > firstOfCur ? firstOfCur : P.blockFirst.slice(0, cur).filter((x) => x != null).pop();
      target = start == null ? 0 : start;
    }
    if (target == null) return;
    if (P.playing) playFrom(target);
    else {
      P.idx = target;
      highlight(target);
      scrollToUnit(target);
      renderPlayer();
    }
  }

  function highlight(idx) {
    $$('.blk.speaking').forEach((n) => n.classList.remove('speaking'));
    $$('.snt.on').forEach((n) => n.classList.remove('on'));
    const u = P.units[idx];
    if (!u) return;
    const blk = $('.blk[data-b="' + u.b + '"]');
    if (blk) blk.classList.add('speaking');
    const sp = $('[data-u="' + idx + '"]');
    if (sp) sp.classList.add('on');
  }

  function scrollToUnit(idx, instant) {
    const u = P.units[idx];
    if (!u) return;
    const sp = $('[data-u="' + idx + '"]') || $('.blk[data-b="' + u.b + '"]');
    const scroller = $('#lec-scroll');
    if (!sp || !scroller) return;
    const blk = sp.closest('.blk') || sp;
    const r = blk.getBoundingClientRect();
    const sr = scroller.getBoundingClientRect();
    const target = scroller.scrollTop + (r.top - sr.top) - sr.height * 0.18;
    scroller.scrollTo({ top: Math.max(0, target), behavior: instant ? 'auto' : 'smooth' });
  }

  function playFrom(idx) {
    if (!P.units.length) {
      toast('This lecture has no narration');
      return;
    }
    const st = Speech.status();
    if (st.native && !st.ready) {
      toast('Voice engine is starting, please try again');
      return;
    }
    if (st.ready === false && !st.native) {
      toast('Speech is not supported here');
      return;
    }
    P.idx = Math.min(Math.max(0, idx), P.units.length - 1);
    P.playing = true;
    P.missingShown = false;
    renderPlayer();
    keepScreenOn(true);
    const items = [];
    for (let i = P.idx; i < P.units.length; i++) items.push(Speech.toItem(i, P.units[i].text));
    Speech.speak(items, prefs.rate, {
      onStart(id) {
        P.idx = id;
        highlight(id);
        scrollToUnit(id);
        store.set('last', { id: P.lec.id, u: id });
        const pl = $('.grow span');
        if (pl) pl.textContent = 'Part ' + (id + 1) + ' of ' + P.units.length;
      },
      onEnd() {},
      onDone() {
        P.playing = false;
        P.idx = 0;
        markDone(P.lec.id);
        keepScreenOn(false);
        $$('.blk.speaking').forEach((n) => n.classList.remove('speaking'));
        $$('.snt.on').forEach((n) => n.classList.remove('on'));
        renderPlayer();
        toast('Lecture finished. Great job!');
      },
      onMissing() {
        if (!P.missingShown) {
          P.missingShown = true;
          const w = $('#voice-warn');
          if (w) w.innerHTML = voiceBanner();
          toast('Urdu voice missing: only English terms can be spoken');
        }
      },
      onError(msg) {
        P.playing = false;
        keepScreenOn(false);
        renderPlayer();
        toast('Speech error' + (msg ? ': ' + msg : ''));
      },
    });
  }

  function pausePlayback() {
    if (!P.playing) return;
    Speech.stop();
    P.playing = false;
    keepScreenOn(false);
    renderPlayer();
  }

  function stopSpeech() {
    Speech.stop();
    P.playing = false;
    keepScreenOn(false);
  }

  function keepScreenOn(on) {
    if (g.AndroidHost) {
      try {
        g.AndroidHost.keepScreenOn(!!on);
      } catch (e) {}
    }
  }

  /* =====================================================================
   *  SETTINGS
   * ===================================================================== */
  function openSettings() {
    const st = Speech.status();
    const bg = $('#sheet-bg');
    const dot = (ok) => '<span class="dotc ' + (ok == null ? '' : ok ? 'ok' : 'no') + '"></span>';
    const seg = (key, opts) =>
      '<div class="seg" data-key="' + key + '">' + opts.map(([v, l, cls]) => '<button data-v="' + v + '" class="' + (String(prefs[key]) === String(v) ? 'on' : '') + ' ' + (cls || '') + '">' + l + '</button>').join('') + '</div>';
    $('#sheet').innerHTML =
      '<h2>Settings <button class="mini-btn" id="s-close" aria-label="Close" style="font-size:18px">&times;</button></h2>' +
      '<div class="set-row"><label>Urdu font</label>' + seg('font', [['naskh', '<span class="ur-sample">نسخ</span> Naskh'], ['nastaliq', '<span class="ur-sample">نستعلیق</span> Nastaliq']]) + '</div>' +
      '<div class="set-row"><label>Text size</label>' + seg('size', [['0.9', 'Small'], ['1', 'Normal'], ['1.15', 'Large'], ['1.3', 'Class mode']]) + '</div>' +
      '<div class="set-row"><label>Theme</label>' + seg('theme', [['auto', 'Auto'], ['light', 'Light'], ['dark', 'Dark']]) + '</div>' +
      '<div class="set-row"><label>Speech speed: <span id="rate-v">' + prefs.rate + 'x</span></label><input type="range" id="rate" min="0.6" max="1.4" step="0.05" value="' + prefs.rate + '"></div>' +
      '<div class="set-row"><label>Voices (Urdish needs two)</label><div class="vstat">' +
      '<div class="line">' + dot(st.ready === false ? null : st.ur) + '<span>Urdu voice (ur-PK): ' + (st.ur ? 'available' : st.ready === false ? 'checking...' : 'not installed') + '</span></div>' +
      '<div class="line">' + dot(st.ready === false ? null : st.en) + '<span>English voice for terms: ' + (st.en ? 'available' : st.ready === false ? 'checking...' : 'not installed') + '</span></div>' +
      '<div class="row-btns"><button class="btn ghost" id="s-test">Test Urdish voice</button>' +
      (Speech.hasNative ? '<button class="btn ghost" data-vi="install">Install voice data</button><button class="btn ghost" data-vi="settings">TTS settings</button>' : '') +
      '</div></div></div>' +
      '<p class="cap" style="text-align:start">Ustad Lectures v1.0 &middot; Offline: MathJax, SVG diagrams and fonts are bundled in the app.</p>';
    bg.classList.add('open');
    sheetOpen = true;
    $('#s-close').onclick = closeSettings;
    $$('#sheet .seg').forEach((s) => {
      $$('button', s).forEach((b) => {
        b.onclick = () => {
          const key = s.dataset.key;
          const v = b.dataset.v;
          prefs[key] = key === 'size' ? parseFloat(v) : v;
          savePrefs();
          $$('button', s).forEach((x) => x.classList.toggle('on', x === b));
          applyPrefs();
        };
      });
    });
    $('#rate').oninput = (e) => {
      prefs.rate = parseFloat(e.target.value);
      $('#rate-v').textContent = prefs.rate + 'x';
      savePrefs();
    };
    $('#rate').onchange = () => {
      if (view === 'lecture') renderPlayer();
    };
    $('#s-test').onclick = () => {
      pausePlayback();
      const sample = 'السلام علیکم بچو! آج ہم Computer Science کا پہلا Lecture پڑھیں گے۔ Algorithm یعنی مسئلہ حل کرنے کا step by step طریقہ۔';
      Speech.speak([Speech.toItem(0, sample)], prefs.rate, {
        onMissing() {
          toast('Urdu voice is not installed on this device');
        },
      });
    };
  }

  function closeSettings() {
    $('#sheet-bg').classList.remove('open');
    sheetOpen = false;
    Speech.stop();
  }
  $('#sheet-bg').addEventListener('click', (e) => {
    if (e.target.id === 'sheet-bg') closeSettings();
  });

  /* =====================================================================
   *  MATHJAX
   * ===================================================================== */
  function typeset(el) {
    const run = () => {
      if (!g.MathJax || !g.MathJax.typesetPromise) return Promise.resolve();
      return g.MathJax.typesetPromise(el ? [el] : undefined).catch((e) => console.warn('MathJax', e.message));
    };
    if (g.MathJax && g.MathJax.startup && g.MathJax.startup.promise) return g.MathJax.startup.promise.then(run);
    return new Promise((res) => {
      let n = 0;
      const t = setInterval(() => {
        n++;
        if (g.MathJax && g.MathJax.startup && g.MathJax.startup.promise) {
          clearInterval(t);
          g.MathJax.startup.promise.then(run).then(res);
        } else if (n > 100) {
          clearInterval(t);
          res();
        }
      }, 100);
    });
  }

  /* =====================================================================
   *  HOST HOOKS + BOOT
   * ===================================================================== */
  g.App = {
    onBack() {
      if (sheetOpen) {
        closeSettings();
        return true;
      }
      if (view === 'lecture') {
        renderHome();
        return true;
      }
      return false;
    },
    onHostPause() {
      if (P.playing) pausePlayback();
    },
    openLecture,
    renderHome,
    typeset,
    state: P,
  };

  function route() {
    const m = /lec=([\w-]+)(?:&u=(\d+))?/.exec(location.hash);
    if (m && Lectures.byId(m[1])) openLecture(m[1], m[2] ? +m[2] : 0);
    else renderHome();
  }

  applyPrefs();
  route();
})(window);
