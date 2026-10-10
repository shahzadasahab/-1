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

  const HEAD_UR = {
    'سیڑھی اور ڈھلوان کی مثال': 'The stairs and ramp analogy',
    'ایک مکمل مثال': 'A complete worked example',
    'قدم بہ قدم مثال': 'A step-by-step example',
    'کتاب کی مثال': 'Textbook example',
    'کتاب کی مثال: عمر کی قسم': 'Textbook example: types of age',
    'مثال: ایک سے N تک کا مجموعہ': 'Example: sum from 1 to N',
    'مثال: تربیت کے اہل فوجی گننا': 'Example: counting eligible soldiers',
    'مثال: نئی زبان سیکھنا': 'Example: learning a new language',
    'دونوں طریقوں کا موازنہ': 'Comparing the two methods',
    'دونوں کا موازنہ': 'Side-by-side comparison',
    'پانچوں طریقوں کا موازنہ': 'Comparing all five methods',
    'خود پہچان کر دیکھیں': 'Try identifying it yourself',
    'ذرا خود کوشش کریں': 'Try this yourself',
    'پورا سفر ایک نظر میں': 'The whole journey at a glance',
    'پورے باب کا خلاصہ': 'Chapter summary',
    'منصوبے کا تعارف': 'Project introduction',
    'چار بڑے ذرائع': 'Four main sources',
    'تعلیم اور صحت': 'Education and healthcare',
    'زبان اور سرکاری خدمات': 'Language and public services',
    'زراعت اور بینکنگ': 'Agriculture and banking',
    'مثبت اور منفی اثرات': 'Positive and negative impacts',
    'سات حفاظتی تدابیر': 'Seven safety measures',
    'پاکستان کی مثالیں': 'Examples from Pakistan',
    'پاکستان کو کیا چاہیے؟': 'What does Pakistan need?',
    'پاکستان کی تعلیم میں AI کا دائرہ': 'The scope of AI in Pakistani education',
    'AI کا خاندان': 'The AI family',
    'اچھا خیال روزمرہ زندگی سے آتا ہے': 'Good ideas come from daily life',
    'ایک آسان مثال: ہوٹل میں آرڈر': 'A simple example: ordering in a hotel',
    'بڑا مسئلہ نہیں، چھوٹا مسئلہ چنیں': 'Pick a small problem, not a huge one',
    'بڑے مسئلے کو چھوٹے حصوں میں توڑنا': 'Breaking a large problem into parts',
    'ظاہری مسئلہ اور اصل مسئلہ': 'The surface problem vs the real problem',
    'مسئلے سے خیال تک پانچ قدم': 'Five steps from problem to idea',
    'مسئلے سے کاروبار تک کا سفر': 'From a problem to a business',
    'لاگت کا اندازہ: ایک ریاضی کی مثال': 'Estimating cost: a numerical example',
    'سب سے زیادہ آنے والا لفظ': 'The most frequent word',
    'کتنا وقت لگتا ہے؟': 'How long does it take?',
    'کتنے موازنے؟': 'How many comparisons?',
    'کون سا طریقہ کہاں؟': 'Which method, and when?',
    'یہ اتنی تیز کیوں ہے؟': 'Why is this so fast?',
    'یہ مہارتیں کہاں کام آتی ہیں؟': 'Where do these skills apply?',
    'نتیجہ': 'Result',
    'اس program کی سمجھ': 'Understanding this program',
    'تینوں operations کی علامتیں': 'Symbols for the three operations',
    'تین gates کا خلاصہ': 'Summary of the three gates',
    'دو variables کے لیے Minterms اور Maxterms': 'Minterms and maxterms for two variables',
    'Access کے Objects': 'Objects in Access',
    'Design View میں table بنانے کے Steps': 'Steps to create a table in Design View',
    'Access کی عام Data Types': 'Common Access data types',
    'Form Wizard کے Steps': 'Form Wizard steps',
    'Simple SELECT Query کے Steps': 'Steps for a simple SELECT query',
    'Grouping Query کے Steps': 'Steps for a grouping query',
    'Average Query کے Steps': 'Steps for an average query',
    'Charts کا موازنہ': 'Comparing the charts',
    'Chart بنانے کا طریقہ': 'How to make a chart',
    'اس علم سے جڑے Careers': 'Careers linked to this topic',
    'پاکستان میں Computing کے استعمال': 'Computing uses in Pakistan',
    'IoT کے استعمال: خلاصہ': 'IoT uses: a summary',
    'Assistive technologies کی اقسام': 'Types of assistive technologies',
    'Importance of Assistive Technologies': 'Importance of assistive technologies',
    'Search operators اور ان کا کام': 'Search operators and what they do',
    'یہ کون سا data ہے؟': 'Which kind of data is this?',
    'یہ Primary ہے یا Secondary؟': 'Is this primary or secondary?',
    'حقیقی زندگی میں Data Analysis': 'Data analysis in real life',
    'Python کیا کر سکتا ہے؟': 'What can Python do?',
    'عام Data Sources': 'Common data sources',
    'پانچ Components': 'Five components',
    'ہوٹل کی مثال اور Components': 'Hotel example and the components',
    'Cursor object کے تین کام': 'Three jobs of a cursor object',
    'نو مراحل اور ان کا کام': 'Nine stages and what they do',
    'Raw data میں تین مسائل': 'Three problems in raw data',
    'DataFrame اہم کیوں ہے؟': 'Why is a DataFrame important?',
    'Missing values کے مراحل': 'Steps for missing values',
    'Missing values کے Pandas Functions': 'Pandas functions for missing values',
    'Function کے key components': 'Key components of a function',
    'File modes کی تفصیل': 'File modes in detail',
    'پڑھنے کے تین طریقے': 'Three ways to read a file',
    'Slicing کے parameters': 'Slicing parameters',
    'چاروں operations کا خلاصہ': 'Summary of the four operations',
    'مشہور پاکستانی digital کاروبار': 'Well-known Pakistani digital businesses',
    'ظاہری مسئلہ بمقابلہ اصل مسئلہ': 'The surface problem vs the real problem',
    'Keys کا موازنہ': 'Comparing the keys',
    'Student table کی مثال': 'Example: a Student table',
    'Side Bar کے حصے': 'Parts of the Side Bar',
    'Python کے بعد کے مواقع': 'What you can do after learning Python',
    'range() کے parameters': 'Parameters of range()',
    'import کے پانچ طریقے': 'Five ways to import',
    'مشہور Third-party Libraries': 'Popular third-party libraries',
    'Discount کا اصول': 'The discount rule',
    'عمر اور نتیجہ': 'Age and the result',
    'Layer 6 کے Key functions': 'Key functions of Layer 6',
    'Transport Layer کے Key functions': 'Key functions of the Transport Layer',
    'Data Link Layer کے Key functions': 'Key functions of the Data Link Layer',
    'Agile چننے کی پانچ وجوہات': 'Five reasons to choose Agile',
    'Sign-up frame کے design elements': 'Design elements of the sign-up frame',
    'فارمولے کی علامتیں': 'Symbols in the formula',
    'Careers کا خلاصہ': 'Careers at a glance',
    'Testing methods کا خلاصہ': 'Testing methods at a glance',
    'Data-collection methods: ایک نظر میں': 'Data-collection methods at a glance',
    'Scenario اور مناسب method': 'Scenario and the matching method',
    'Case study کے visuals': 'Visuals in this case study',
    'Artefact options اور tools': 'Artefact options and tools',
    'Survey کے سوالات کی اقسام اور ان سے ملنے والا data': 'Survey question types and the data they give',
  };

  function titleCase(s) {
    return s
      .replace(/\s+/g, ' ')
      .trim()
      .replace(/^(and|or|of|the|:)\s+/i, '')
      .replace(/\b([a-z])/g, (m) => m.toUpperCase())
      .replace(/\b(And|Or|Of|The|Vs|To|For|In|On|A|An)\b/g, (m) => m.toLowerCase())
      .replace(/^[a-z]/, (m) => m.toUpperCase());
  }

  function collectTerms(text) {
    const terms = [];
    const seen = {};
    String(text || '').replace(/\*\*([^*]+)\*\*/g, (_, t) => {
      const k = t.trim();
      if (k && /[A-Za-z]/.test(k) && !seen[k.toLowerCase()]) {
        seen[k.toLowerCase()] = 1;
        terms.push(k);
      }
      return _;
    });
    if (!terms.length) {
      String(text || '').replace(LATIN_RUN, (m) => {
        if (m.length < 3 || seen[m.toLowerCase()]) return m;
        if (/^(the|and|for|with|from|this|that|then|you|are|was|can|has|had|not|but)$/i.test(m)) return m;
        seen[m.toLowerCase()] = 1;
        terms.push(m);
        return m;
      });
    }
    return terms;
  }

  /** English-only heading for display. Narration still uses the Urdish `ur`. */
  function headingEn(ur, explicit) {
    if (explicit && /[A-Za-z]/.test(explicit)) return explicit.replace(/\s+/g, ' ').trim();
    const raw = String(ur || '').trim();
    if (HEAD_UR[raw]) return HEAD_UR[raw];
    const what = /کیا ہے\s*\??|کیا ہوتے ہیں\s*\??/.test(raw);
    const why = /کیوں/.test(raw);
    const how = /کیسے|کا طریقہ/.test(raw);
    let s = raw
      .replace(/کیا ہے\s*\??/g, '')
      .replace(/کیا ہوتے ہیں\s*\??/g, '')
      .replace(/اور/g, ' and ')
      .replace(/یعنی/g, ': ')
      .replace(/کی پہچان/g, '')
      .replace(/کا طریقہ/g, '')
      .replace(/کیسے کام کرتا ہے\s*\??/g, '')
      .replace(/کیسے/g, '')
      .replace(/کیوں/g, '')
      .replace(/کی مثال(یں)?/g, ' — example')
      .replace(/کا خلاصہ/g, ' summary')
      .replace(/کی وجوہات/g, ' reasons')
      .replace(/کی اقسام/g, ' types')
      .replace(/کی خصوصیات/g, ' features')
      .replace(/کی تعریف/g, '')
      .replace(/کی اہمیت/g, ' importance')
      .replace(/بمقابلہ/g, ' vs ')
      .replace(/کے Steps/g, ' steps')
      .replace(/کے parameters/g, ' parameters')
      .replace(/کے Key functions/g, ' key functions')
      .replace(/والا/g, '')
      .replace(/والے/g, '')
      .replace(/والی/g, '')
      .replace(/[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]+/g, ' ')
      .replace(/[،۔؟]/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
    if (s.length < 2) return '';
    s = titleCase(s);
    if (what && !/^What\b/i.test(s)) s = 'What is ' + s.replace(/\?$/, '') + '?';
    else if (why && !/^Why\b/i.test(s)) s = 'Why ' + s.replace(/\?$/, '') + '?';
    else if (how && !/^How\b/i.test(s)) s = 'How ' + s.replace(/\?$/, '') + ' works';
    return s;
  }

  /** Compact English terms (chips / fallback). Not spoken. */
  function keyIdea(text) {
    const terms = collectTerms(text);
    if (!terms.length) return '';
    return terms.slice(0, 6).join('  ·  ');
  }

  /**
   * Full English display line for a Urdish block.
   * Uses an explicit `en` field when the author wrote one; otherwise builds
   * a short English sentence from terms. Never used for TTS.
   */
  function displayEn(text, explicit) {
    if (explicit && /[A-Za-z]/.test(explicit)) return explicit.replace(/\s+/g, ' ').trim();
    const raw = String(text || '');
    if (!raw) return '';
    const terms = collectTerms(raw).slice(0, 5);
    const greeting = /السلام علیکم/.test(raw);
    const isDef = /Definition:|تعریف|کہتے ہیں/.test(raw);
    const isEx = /مثال/.test(raw);
    const isWhy = /کیوں/.test(raw);
    const isHow = /کیسے|طریقہ/.test(raw);
    const isCmp = /موازنہ|فرق|بمقابلہ/.test(raw);
    const isQ = /کیا ہے|کیا ہوتے ہیں/.test(raw);

    if (!terms.length) {
      if (greeting) return 'Welcome. Read the English idea, then hear the teacher in Urdish.';
      const h = headingEn(raw, '');
      return h || '';
    }
    const main = terms[0];
    const rest = terms.slice(1);
    const extra = rest.length ? ': ' + rest.join(', ') : '';
    if (greeting) return 'Welcome. Today’s idea — ' + terms.join(', ') + '.';
    if (isDef) return main + (rest.length ? ' means ' + rest.join(', ') : ' — definition') + '.';
    if (isQ && !isWhy && !isHow) return 'What is ' + main + (rest.length ? ' (' + rest.join(', ') + ')' : '') + '?';
    if (isWhy) return 'Why ' + terms.join(' and ') + ' matter.';
    if (isHow) return 'How ' + main + ' works' + extra + '.';
    if (isEx) return 'Example: ' + terms.join(', ') + '.';
    if (isCmp) return 'Compare ' + terms.join(' vs ') + '.';
    if (terms.length === 1) return 'This part explains ' + main + '.';
    return 'This part explains ' + main + extra + '.';
  }

  g.Chapters = CHAPTERS;
  g.Lectures = Lectures;
  g.Diagrams = Diagrams;
  g.U = { esc, inline, headingEn, keyIdea, displayEn };
})(typeof window !== 'undefined' ? window : globalThis);
