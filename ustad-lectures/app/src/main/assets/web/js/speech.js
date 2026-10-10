/* Urdish speech: turns lecture markup into language-tagged runs and plays them
 * through Android TextToSpeech (AndroidTTS bridge) or the browser speechSynthesis fallback.
 *
 * Urdish = Urdu script narration + English technical terms in Latin script.
 * Urdu runs are spoken with an Urdu voice and English runs with an English voice.
 */
(function (g) {
  'use strict';

  const AR = /[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]/;
  const LAT = /[A-Za-z]/;

  const PRON = {
    'TCP/IP': 'T C P I P',
    TCP: 'T C P',
    UDP: 'U D P',
    HTTP: 'H T T P',
    HTTPS: 'H T T P S',
    FTP: 'F T P',
    DNS: 'D N S',
    DHCP: 'D H C P',
    IP: 'I P',
    SDLC: 'S D L C',
    OSI: 'O S I',
    SQL: 'S Q L',
    SQLite: 'S Q Lite',
    DBMS: 'D B M S',
    RDBMS: 'R D B M S',
    HCI: 'H C I',
    UI: 'U I',
    UX: 'U X',
    AI: 'A I',
    IoT: 'I O T',
    ML: 'M L',
    CPU: 'C P U',
    RAM: 'RAM',
    API: 'A P I',
    MVP: 'M V P',
    CSV: 'C S V',
    IDE: 'I D E',
    PK: 'P K',
    FK: 'F K',
    ER: 'E R',
    ERD: 'E R D',
    XOR: 'X OR',
    XNOR: 'X NOR',
    NAND: 'NAND',
    'K-Map': 'K Map',
    'K-Maps': 'K Maps',
    JSON: 'Jason',
    GUI: 'G U I',
    PDF: 'P D F',
    USB: 'U S B',
    LAN: 'LAN',
    WAN: 'WAN',
    VPN: 'V P N',
    DDoS: 'D Dos',
    NN: 'N N',
    DL: 'D L',
    CNN: 'C N N',
    RNN: 'R N N',
    LogiSim: 'Logi Sim',
    pandas: 'pandas',
    matplotlib: 'mat plot lib',
    numpy: 'num pie',
    Figma: 'Figma',
    'Big-O': 'Big O',
  };

  const NUMW = { 0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine' };

  /** TeX -> short English phrase (used when a math block has no `say`). */
  function texToSpeech(tex) {
    let s = ' ' + tex + ' ';
    const rep = (re, to) => {
      s = s.replace(re, to);
    };
    for (let i = 0; i < 4; i++) {
      rep(/\\(?:overline|bar|bar|neg)\s*\{([^{}]*)\}/g, ' NOT $1 ');
      rep(/\\(?:text|mathrm|mathbf|textbf|mathit|operatorname)\s*\{([^{}]*)\}/g, ' $1 ');
      rep(/\\frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}/g, ' $1 over $2 ');
      rep(/\\sqrt\s*\{([^{}]*)\}/g, ' square root of $1 ');
      rep(/\^\s*\{?\s*2\s*\}?/g, ' squared ');
      rep(/\^\s*\{?\s*3\s*\}?/g, ' cubed ');
      rep(/\^\s*\{([^{}]*)\}/g, ' to the power $1 ');
      rep(/\^\s*([A-Za-z0-9])/g, ' to the power $1 ');
      rep(/_\s*\{([^{}]*)\}/g, ' sub $1 ');
      rep(/_\s*([A-Za-z0-9])/g, ' sub $1 ');
    }
    const map = [
      [/\\overline\s*([A-Za-z0-9])/g, ' NOT $1 '],
      [/\\bar\s*([A-Za-z0-9])/g, ' NOT $1 '],
      [/\\cdot|\\land|\\wedge/g, ' AND '],
      [/\\lor|\\vee/g, ' OR '],
      [/\\lnot|\\neg/g, ' NOT '],
      [/\\oplus/g, ' XOR '],
      [/\\odot/g, ' XNOR '],
      [/\\times/g, ' times '],
      [/\\div/g, ' divided by '],
      [/\\leq?|\\le\b/g, ' less than or equal to '],
      [/\\geq?|\\ge\b/g, ' greater than or equal to '],
      [/\\neq|\\ne\b/g, ' not equal to '],
      [/\\approx/g, ' approximately '],
      [/\\(?:to|rightarrow|Rightarrow|implies)/g, ' gives '],
      [/\\sum/g, ' sum of '],
      [/\\log/g, ' log '],
      [/\\infty/g, ' infinity '],
      [/\\pm/g, ' plus or minus '],
      [/\\sigma/g, ' sigma '],
      [/\\mu/g, ' mu '],
      [/\\(?:left|right)/g, ' '],
      [/\\[,;:! ]/g, ' '],
      [/\\ldots|\\dots|\\cdots/g, ' dot dot dot '],
      [/\\([A-Za-z]+)/g, ' $1 '],
      [/\+/g, ' plus '],
      [/=/g, ' equals '],
      [/</g, ' less than '],
      [/>/g, ' greater than '],
      [/\*/g, ' times '],
      [/\|/g, ' mod '],
      [/[{}]/g, ' '],
      [/'/g, ' bar '],
    ];
    map.forEach(([re, to]) => rep(re, to));
    rep(/(?<![A-Za-z0-9])-(?=\s*[A-Za-z0-9])/g, ' minus ');
    rep(/(?<=[A-Za-z0-9)])\s*-\s*(?=[A-Za-z0-9(])/g, ' minus ');
    rep(/\s+/g, ' ');
    return s.trim();
  }

  /** Lecture markup -> plain spoken text (math rendered as English words). */
  function plain(text) {
    return String(text)
      .replace(/\$([^$]+)\$/g, (m, t) => ' ' + texToSpeech(t) + ' ')
      .replace(/\*\*([^*]+)\*\*/g, '$1')
      .replace(/`([^`]+)`/g, '$1')
      .replace(/[→⇒]/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
  }

  const PRON_RE = new RegExp(
    '(?<![A-Za-z0-9])(' +
      Object.keys(PRON)
        .sort((a, b) => b.length - a.length)
        .map((k) => k.replace(/[.*+?^${}()|[\]\\\/-]/g, '\\$&'))
        .join('|') +
      ')(?![A-Za-z0-9])',
    'g'
  );

  function fixEnglish(t) {
    return t
      .replace(PRON_RE, (m) => PRON[m] || m)
      .replace(/(\d+)\.(\d+)/g, '$1 point $2')
      .replace(/\//g, ' slash ')
      .replace(/[_#]/g, ' ')
      .replace(/&/g, ' and ')
      .replace(/\s+/g, ' ');
  }

  /** Split plain text into language runs: [{l:'ur'|'en', t:'...'}] */
  function runs(text) {
    const out = [];
    let cur = null;
    let lead = '';
    for (const ch of text) {
      let l = null;
      if (AR.test(ch)) l = 'ur';
      else if (LAT.test(ch)) l = 'en';
      if (l === null) {
        if (cur) cur.t += ch;
        else lead += ch;
        continue;
      }
      if (!cur || cur.l !== l) {
        cur = { l, t: '' };
        out.push(cur);
        if (lead) {
          cur.t = lead;
          lead = '';
        }
      }
      cur.t += ch;
    }
    return out
      .map((r) => ({ l: r.l, t: r.l === 'en' ? fixEnglish(r.t).trim() : r.t.trim() }))
      .filter((r) => /[A-Za-z0-9\u0621-\u063A\u0641-\u064A\u0660-\u0669\u066E-\u06D3\u06F0-\u06F9]/.test(r.t));
  }

  function splitSentences(text) {
    const t = String(text).trim();
    if (!t) return [];
    const pieces = t.split(/(?<=[۔؟!?])\s+|(?<=\.)\s+(?=[A-Z\u0600-\u06FF])|\n+/);
    const out = [];
    pieces.forEach((p) => {
      p = p.trim();
      if (!p) return;
      if (p.length > 260) {
        const sub = p.split(/(?<=[،,;؛])\s+/);
        let acc = '';
        sub.forEach((s) => {
          if ((acc + ' ' + s).length > 200 && acc) {
            out.push(acc);
            acc = s;
          } else acc = acc ? acc + ' ' + s : s;
        });
        if (acc) out.push(acc);
      } else out.push(p);
    });
    return out;
  }

  /* ---------------- engine ---------------- */

  const hasNative = typeof g.AndroidTTS !== 'undefined';
  let jobSeq = 0;
  let handlers = null;
  let activeJob = 0;
  let statusCache = { native: hasNative, ready: !hasNative, ur: null, en: null };

  function nativeStatus() {
    try {
      return JSON.parse(g.AndroidTTS.status());
    } catch (e) {
      return { native: true, ready: false };
    }
  }

  function webVoices() {
    const v = (g.speechSynthesis && g.speechSynthesis.getVoices()) || [];
    return {
      ur: v.find((x) => /^ur/i.test(x.lang)) || null,
      en: v.find((x) => /^en[-_]IN/i.test(x.lang)) || v.find((x) => /^en/i.test(x.lang)) || null,
    };
  }

  function status() {
    if (hasNative) {
      statusCache = nativeStatus();
      return statusCache;
    }
    const ok = !!g.speechSynthesis;
    const v = ok ? webVoices() : { ur: null, en: null };
    statusCache = { native: false, ready: ok, ur: !!v.ur, en: !!v.en, engine: 'browser' };
    return statusCache;
  }

  /** items: [{id, segs:[{l,t}]}] */
  function speak(items, rate, h) {
    stop(true);
    const job = ++jobSeq;
    activeJob = job;
    handlers = h || {};
    if (hasNative) {
      g.AndroidTTS.speak(job, JSON.stringify(items), rate);
      return job;
    }
    webSpeak(job, items, rate);
    return job;
  }

  function webSpeak(job, items, rate) {
    const synth = g.speechSynthesis;
    if (!synth) {
      setTimeout(() => handlers && handlers.onError && handlers.onError('nosynth'), 0);
      return;
    }
    const voices = webVoices();
    let ii = 0;
    let si = 0;
    const next = () => {
      if (job !== activeJob) return;
      if (ii >= items.length) {
        handlers.onDone && handlers.onDone();
        return;
      }
      const it = items[ii];
      if (si === 0) handlers.onStart && handlers.onStart(it.id);
      if (si >= it.segs.length) {
        handlers.onEnd && handlers.onEnd(it.id);
        ii++;
        si = 0;
        return next();
      }
      const seg = it.segs[si++];
      const voice = voices[seg.l];
      if (!voice) {
        if (seg.l === 'ur') handlers.onMissing && handlers.onMissing('ur');
        return next();
      }
      const u = new SpeechSynthesisUtterance(seg.t);
      u.voice = voice;
      u.lang = voice.lang;
      u.rate = rate;
      u.onend = next;
      u.onerror = () => {
        if (job === activeJob) next();
      };
      synth.speak(u);
    };
    synth.cancel();
    next();
  }

  function stop(silent) {
    activeJob = ++jobSeq;
    if (hasNative) {
      try {
        g.AndroidTTS.stop();
      } catch (e) {}
    } else if (g.speechSynthesis) g.speechSynthesis.cancel();
    if (!silent) handlers = null;
  }

  g.__tts = {
    onNative(o) {
      const h = handlers;
      if (!h || o.job !== activeJob) return;
      if (o.type === 'start') h.onStart && h.onStart(o.id);
      else if (o.type === 'end') h.onEnd && h.onEnd(o.id);
      else if (o.type === 'done') h.onDone && h.onDone();
      else if (o.type === 'missing') h.onMissing && h.onMissing(o.msg);
      else if (o.type === 'error') h.onError && h.onError(o.msg);
    },
  };

  g.Speech = {
    plain,
    texToSpeech,
    runs,
    splitSentences,
    status,
    speak,
    stop,
    hasNative,
    openVoiceSettings() {
      if (hasNative) g.AndroidTTS.openVoiceSettings();
    },
    installVoiceData() {
      if (hasNative) g.AndroidTTS.installVoiceData();
    },
    refresh() {
      if (hasNative) g.AndroidTTS.refresh();
    },
    toItem(id, markup) {
      return { id, segs: runs(plain(markup)) };
    },
  };

  if (!hasNative && g.speechSynthesis) g.speechSynthesis.onvoiceschanged = () => {};
})(typeof window !== 'undefined' ? window : globalThis);
