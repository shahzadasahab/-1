/* Core registries shared by every lecture / diagram file. */
(function (g) {
  'use strict';

  const CHAPTERS = [
    { cls: 'XI', ch: 1, en: 'Computer Systems', ur: 'کمپیوٹر سسٹمز', sub: 'Digital Logic, SDLC, OSI & TCP/IP', color: 0 },
    { cls: 'XI', ch: 2, en: 'Computational Thinking and Algorithms', ur: 'کمپیوٹیشنل تھنکنگ اور الگورتھمز', sub: 'Algorithms, Sorting, Searching', color: 1 },
    { cls: 'XI', ch: 3, en: 'Programming Fundamentals', ur: 'پروگرامنگ کے بنیادی اصول', sub: 'Python basics, Control flow, Libraries', color: 2 },
    { cls: 'XI', ch: 4, en: 'Data and Analysis', ur: 'ڈیٹا اور تجزیہ', sub: 'Databases, ER Model, Access Queries', color: 3 },
    { cls: 'XI', ch: 5, en: 'Applications and Impacts of Computing', ur: 'کمپیوٹنگ کے استعمالات اور اثرات', sub: 'AI, IoT, Data Analytics, Careers', color: 4 },
    { cls: 'XI', ch: 6, en: 'Digital Literacy', ur: 'ڈیجیٹل خواندگی', sub: 'Data collection, Presentation, Research', color: 5 },
    { cls: 'XII', ch: 1, en: 'Human Computer Interaction', ur: 'ہیومن کمپیوٹر انٹرایکشن', sub: 'HCI, UI/UX, Wireframing, Figma', color: 0 },
    { cls: 'XII', ch: 2, en: 'Computational Thinking and Algorithms', ur: 'کمپیوٹیشنل تھنکنگ اور الگورتھمز', sub: 'Tracing, Efficiency, Data Structures', color: 1 },
    { cls: 'XII', ch: 3, en: 'Programming Fundamentals', ur: 'پروگرامنگ کے بنیادی اصول', sub: 'Lists, Tuples, Sets, Dicts, Functions, Files', color: 2 },
    { cls: 'XII', ch: 4, en: 'Data and Analysis', ur: 'ڈیٹا اور تجزیہ', sub: 'SQLite, DataFrames, Visualization, Statistics', color: 3 },
    { cls: 'XII', ch: 5, en: 'Applications and Impacts of Computing', ur: 'کمپیوٹنگ کے استعمالات اور اثرات', sub: 'Neural Networks, Deep Learning, Security', color: 4 },
    { cls: 'XII', ch: 6, en: 'Entrepreneurship in the Digital Age', ur: 'ڈیجیٹل دور میں انٹرپرینیورشپ', sub: 'Ideas, Prototypes, MVP', color: 5 },
  ];

  const Lectures = {
    list: [],
    add(l) {
      this.list.push(l);
    },
    byId(id) {
      return this.list.find((x) => x.id === id);
    },
    sorted() {
      const order = (l) => (l.cls === 'XI' ? 0 : 1) * 1e6 + l.ch * 1e3 + (l.n || 0);
      return this.list.slice().sort((a, b) => order(a) - order(b) || a.id.localeCompare(b.id));
    },
    forChapter(cls, ch) {
      return this.sorted().filter((l) => l.cls === cls && l.ch === ch);
    },
  };

  const Diagrams = {
    reg: {},
    register(id, fn) {
      if (this.reg[id]) console.warn('duplicate diagram id ' + id);
      this.reg[id] = fn;
    },
    has(id) {
      return !!this.reg[id];
    },
    render(id, args) {
      const fn = this.reg[id];
      if (!fn) return '<div class="dg-missing">diagram "' + id + '" not found</div>';
      try {
        return fn(args || {});
      } catch (e) {
        return '<div class="dg-missing">diagram error: ' + id + ' ' + e.message + '</div>';
      }
    },
  };

  const esc = (s) =>
    String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

  const WORD = "[(\\[]?[A-Za-z0-9][A-Za-z0-9+#_\\-\\/&']*(?:\\.(?=[A-Za-z0-9])[A-Za-z0-9+#_\\-\\/&']*)*[)\\]]?";
  const LATIN_RUN = new RegExp(WORD + '(?:,? +' + WORD + ')*', 'g');

  /**
   * Inline markup -> safe HTML.
   *   $tex$    inline MathJax          **text** bold term        `code` inline code
   * Latin runs inside Urdu text are isolated as LTR so English terms keep their order.
   */
  function inline(text) {
    const parts = String(text).split(/(\$[^$]+\$|\*\*[^*]+\*\*|`[^`]+`)/g);
    return parts
      .map((p) => {
        if (!p) return '';
        if (p[0] === '$' && p.length > 2) return '<span class="im" dir="ltr">\\(' + esc(p.slice(1, -1)) + '\\)</span>';
        if (p.startsWith('**') && p.length > 4) return '<strong>' + latin(p.slice(2, -2)) + '</strong>';
        if (p[0] === '`' && p.length > 2) return '<code class="ic" dir="ltr">' + esc(p.slice(1, -1)) + '</code>';
        return latin(p);
      })
      .join('');
  }

  function latin(raw) {
    let out = '';
    let last = 0;
    raw.replace(LATIN_RUN, (m, off) => {
      out += esc(raw.slice(last, off)) + '<span class="en" dir="ltr">' + esc(m) + '</span>';
      last = off + m.length;
      return m;
    });
    return out + esc(raw.slice(last));
  }

  g.Chapters = CHAPTERS;
  g.Lectures = Lectures;
  g.Diagrams = Diagrams;
  g.U = { esc, inline };
})(typeof window !== 'undefined' ? window : globalThis);
