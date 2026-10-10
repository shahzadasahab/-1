/* XI Ch6 (Digital Literacy) diagrams */
(function () {
  const D = Diagrams;

  const tick = (x, y, cls) => K.path('M' + x + ' ' + y + ' l5 6 l10 -12', { s: cls || 's-grn', w: 3 });

  D.register('xi6.literacy-skills', () => {
    let s = '';
    const items = [
      ['Find information', 0, 0],
      ['Communicate', 1, 0],
      ['Produce content', 0, 1],
      ['Solve problems', 1, 1],
      ['Organize data', 0, 2],
      ['Share responsibly', 1, 2],
    ];
    const cx = 220;
    const cy = 105;
    items.forEach(([label, side, row], i) => {
      const x = side ? 316 : 4;
      const y = 8 + row * 80;
      s += K.line(side ? x : x + 120, y + 20, cx + (side ? 46 : -46), cy + (row - 1) * 22, { cls: 's-mut', dash: '4 3' });
      s += K.box(x, y, 120, 40, label, { c: [0, 1, 4, 3, 5, 2][i], size: 13 });
    });
    s += K.circle(cx, cy, 48, { c: 7 });
    s += K.text(cx, cy - 6, 'Digital', { size: 14, w: 'b' });
    s += K.text(cx, cy + 12, 'Literacy', { size: 14, w: 'b' });
    return K.svg(440, 215, s, { title: 'Digital literacy: find, evaluate, organize, create, communicate and share information responsibly' });
  });

  D.register('xi6.search-operators', () => {
    let s = '';
    const rows = [
      ['" "', 'Quotation marks', '"mobile phone use" "study habits" students', 'Exact phrase only', 1],
      ['filetype:', 'File type', 'student screen time and learning filetype:pdf', 'Only PDF documents', 3],
      ['site:', 'Website / domain', 'digital distraction students site:.edu', 'Only that domain', 5],
    ];
    rows.forEach(([op, name, q, what, c], i) => {
      const y = 8 + i * 84;
      s += K.rect(4, y, 432, 74, { c: 6, r: 10 });
      s += K.box(12, y + 10, 92, 54, op, { c, size: 15, bold: true });
      s += K.text(116, y + 22, name, { size: 12, anchor: 'start', w: 'b', cls: 't-acc' });
      s += K.text(116, y + 43, q, { size: 12, anchor: 'start' });
      s += K.text(116, y + 63, '= ' + what, { size: 12, anchor: 'start', cls: 't-mut' });
    });
    return K.svg(440, 262, s, { title: 'Advanced search operators: quotation marks, filetype and site with example queries' });
  });

  D.register('xi6.source-check', () => {
    let s = '';
    const q = [
      'Is the author or organization clearly mentioned?',
      'Is the information recent?',
      'Is the website reliable: educational,\ngovernment or research-based?',
      'Does it give facts, data or references?',
      'Is it balanced and not biased?',
    ];
    q.forEach((t, i) => {
      const y = 8 + i * 52;
      s += K.rect(4, y, 432, 44, { c: i % 2 ? 6 : 1, r: 10 });
      s += K.circle(28, y + 22, 13, { c: 4 });
      s += K.text(28, y + 22, String(i + 1), { size: 13, w: 'b', vmid: true });
      s += K.text(52, y + 22, t, { size: 12, anchor: 'start', vmid: true });
      s += tick(402, y + 22);
    });
    s += K.text(220, 285, 'Mostly YES means: a trustworthy source', { size: 13, w: 'b', cls: 't-grn' });
    return K.svg(440, 296, s, { title: 'Source evaluation checklist with five questions' });
  });

  D.register('xi6.qual-quant', () => {
    let s = '';
    s += K.rect(4, 6, 212, 230, { c: 3, r: 12 });
    s += K.rect(224, 6, 212, 230, { c: 1, r: 12 });
    s += K.text(110, 30, 'Qualitative', { size: 15, w: 'b' });
    s += K.text(330, 30, 'Quantitative', { size: 15, w: 'b' });
    s += K.text(110, 54, 'Words, opinions,\nreasons, behaviour', { size: 12 });
    s += K.text(330, 54, 'Numbers: count,\nmeasure, compare', { size: 12 });
    s += K.rect(20, 92, 180, 74, { c: 4, r: 14 });
    s += K.poly([[44, 166], [62, 166], [40, 184]], { c: 4 });
    s += K.text(110, 129, '"Online classes are tiring,\nbut I can replay lectures."', { size: 12, vmid: true });
    s += K.rect(240, 92, 180, 28, { c: 0, r: 6 }) + K.text(330, 107, '2 hours online per day', { size: 12, vmid: true });
    s += K.rect(240, 126, 180, 28, { c: 0, r: 6 }) + K.text(330, 141, '42 out of 50 marks', { size: 12, vmid: true });
    s += K.rect(240, 160, 180, 28, { c: 0, r: 6 }) + K.text(330, 175, '35% study with phone', { size: 12, vmid: true });
    s += K.text(110, 206, 'WHY and HOW?', { size: 14, w: 'b', cls: 't-acc' });
    s += K.text(110, 224, 'Understand reasons', { size: 11, cls: 't-mut' });
    s += K.text(330, 206, 'HOW MANY / HOW MUCH?', { size: 14, w: 'b', cls: 't-acc' });
    s += K.text(330, 224, 'Charts and averages', { size: 11, cls: 't-mut' });
    return K.svg(440, 244, s, { title: 'Qualitative data describes opinions in words; quantitative data is numbers' });
  });

  D.register('xi6.research-process', (args) => {
    args = args || {};
    let s = '';
    const st = [
      ['Question', 'What do we\nwant to\nknow?', 1],
      ['Search', 'Find\nreliable\nsources', 0],
      ['Collect', 'Survey or\ninterview', 5],
      ['Analyze', 'Use spreadsheet,\ncharts', 4],
      ['Create', 'Report, slides\nor infographic', 2],
    ];
    const w = 72;
    const gap = 17;
    st.forEach(([n, d, c], i) => {
      const x = 4 + i * (w + gap);
      s += K.circle(x + w / 2, 18, 11, { c: 7 }) + K.text(x + w / 2, 18, String(i + 1), { size: 12, w: 'b', vmid: true });
      s += K.box(x, 38, w, 44, n, { c, size: 13, bold: true });
      s += K.text(x + w / 2, 104, d, { size: 11, cls: 't-mut' });
      if (i < st.length - 1) s += K.line(x + w + 1, 60, x + w + gap - 1, 60, { arrow: true, w: 1.4 });
    });
    s += K.rect(4, 156, 432, 36, { c: 6, r: 10 });
    s += K.text(220, 174, args.note || 'Digital inquiry workflow: from research question to final artefact', { size: 12, vmid: true, cls: 't-mut' });
    return K.svg(440, 200, s, { title: 'Digital inquiry workflow: question, search, collect, analyze, create' });
  });

  D.register('xi6.methods-map', () => {
    let s = '';
    const top = [
      ['Interviews', 'Planned talk with\na person', 3],
      ['Surveys', 'Same questions to\nmany people', 1],
      ['Prototypes', 'Early version tested\nby users', 4],
    ];
    top.forEach(([n, d, c], i) => {
      const x = 4 + i * 148;
      s += K.rect(x, 8, 140, 70, { c, r: 10 });
      s += K.text(x + 70, 28, n, { size: 14, w: 'b' });
      s += K.text(x + 70, 48, d, { size: 11 });
      s += K.line(x + 70, 78, 220, 118, { cls: 's-mut', dash: '4 3' });
    });
    s += K.box(130, 106, 180, 40, 'Data collection', { c: 7, size: 15, bold: true });
    const bot = [
      ['Observation', 'Watch and record\nwhat happens', 5, 40],
      ['Simulations', 'Computer model;\nchange variables', 2, 244],
    ];
    bot.forEach(([n, d, c, x]) => {
      s += K.rect(x, 176, 156, 70, { c, r: 10 });
      s += K.text(x + 78, 196, n, { size: 14, w: 'b' });
      s += K.text(x + 78, 216, d, { size: 11 });
      s += K.line(220, 146, x + 78, 176, { cls: 's-mut', dash: '4 3' });
    });
    return K.svg(440, 256, s, { title: 'Five data-collection methods: interviews, surveys, prototypes, observation, simulations' });
  });

  D.register('xi6.survey-form', () => {
    let s = '';
    const radio = (x, y, label, on) => {
      let o = K.circle(x, y, 7, { c: on ? 4 : null });
      if (on) o += K.dot(x, y, 3);
      return o + K.text(x + 13, y, label, { size: 12, anchor: 'start', vmid: true });
    };
    const check = (x, y, label, on) => {
      let o = K.rect(x - 7, y - 7, 14, 14, { c: on ? 4 : null, r: 3 });
      if (on) o += K.path('M' + (x - 4) + ' ' + y + ' l3 4 l6 -8', { w: 2 });
      return o + K.text(x + 13, y, label, { size: 12, anchor: 'start', vmid: true });
    };
    s += K.rect(4, 4, 300, 372, { c: 6, r: 12 });
    s += K.rect(4, 4, 300, 44, { c: 1, r: 12 });
    s += K.text(154, 20, 'Digital Literacy Survey', { size: 14, w: 'b' });
    s += K.text(154, 37, 'Google Forms / Microsoft Forms', { size: 11, cls: 't-mut' });
    s += K.text(14, 66, '1. Do you use a computer or phone daily?', { size: 12, anchor: 'start', w: 'b' });
    s += radio(26, 88, 'Yes', true) + radio(96, 88, 'No', false);
    s += K.text(14, 120, '2. How often do you use the internet to study?', { size: 12, anchor: 'start', w: 'b' });
    s += radio(26, 142, 'Daily', true) + radio(110, 142, 'A few times a week', false);
    s += radio(26, 164, 'Rarely', false) + radio(110, 164, 'Never', false);
    s += K.text(14, 196, '3. Which devices do you use most?', { size: 12, anchor: 'start', w: 'b' });
    s += check(26, 218, 'Smartphone', true) + check(130, 218, 'Laptop', true);
    s += check(26, 240, 'Desktop computer', false) + check(166, 240, 'Tablet', false);
    s += check(26, 262, 'Other', false);
    s += K.text(14, 296, '4. How does your phone help you study?', { size: 12, anchor: 'start', w: 'b' });
    s += K.rect(14, 308, 280, 54, { c: null, r: 6 });
    s += K.text(24, 326, 'Type your answer here...', { size: 12, anchor: 'start', cls: 't-mut' });
    s += K.text(372, 86, 'Single choice', { size: 12, w: 'b' }) + K.text(372, 102, 'Quantitative', { size: 12, cls: 't-acc' });
    s += K.text(372, 150, 'Single choice', { size: 12, w: 'b' }) + K.text(372, 166, 'Quantitative', { size: 12, cls: 't-acc' });
    s += K.text(372, 230, 'Multiple choice', { size: 12, w: 'b' }) + K.text(372, 246, 'Quantitative', { size: 12, cls: 't-acc' });
    s += K.text(372, 326, 'Open-ended', { size: 12, w: 'b' }) + K.text(372, 342, 'Qualitative', { size: 12, cls: 't-red' });
    [88, 154, 232, 328].forEach((y) => {
      s += K.line(306, y, 322, y, { cls: 's-mut', w: 1.4 });
    });
    return K.svg(440, 380, s, { title: 'A sample online survey form with single-choice, multiple-choice and open-ended questions' });
  });

  D.register('xi6.prototype-loop', () => {
    let s = '';
    const b = [
      ['1. Build a simple\nprototype', 30, 14, 4],
      ['2. Users try\nthe prototype', 260, 14, 1],
      ['3. Users give\nfeedback', 260, 124, 3],
      ['4. Improve the\nidea', 30, 124, 5],
    ];
    b.forEach(([t, x, y, c]) => {
      s += K.box(x, y, 150, 56, t, { c, size: 13 });
    });
    s += K.line(182, 42, 258, 42, { arrow: true });
    s += K.line(335, 72, 335, 122, { arrow: true });
    s += K.line(258, 152, 182, 152, { arrow: true });
    s += K.line(105, 122, 105, 72, { arrow: true });
    s += K.text(220, 99, 'Feedback = data', { size: 13, w: 'b', cls: 't-acc' });
    s += K.text(220, 114, 'repeat until ready', { size: 11, cls: 't-mut' });
    s += K.text(220, 202, 'Test the idea before spending time on the final version', { size: 12, cls: 't-mut' });
    return K.svg(440, 214, s, { title: 'Prototype cycle: build, users try, feedback, improve' });
  });

  D.register('xi6.simulation', () => {
    let s = '';
    s += K.box(4, 34, 110, 90, 'Real situation\n(costly, risky\nor difficult)', { c: 3, size: 12 });
    s += K.line(116, 79, 150, 79, { arrow: true });
    s += K.rect(152, 10, 150, 138, { c: 0, r: 12 });
    s += K.text(227, 28, 'Computer model', { size: 13, w: 'b' });
    [['Cars per minute', 44, 0.35], ['Green light time', 80, 0.7], ['Number of lanes', 116, 0.5]].forEach(([l, y, f]) => {
      s += K.text(227, y - 6, l, { size: 11, cls: 't-mut' });
      s += K.line(168, y + 6, 286, y + 6, { cls: 's-mut', w: 2.5 });
      s += K.circle(168 + 118 * f, y + 6, 6, { c: 4 });
    });
    s += K.line(304, 79, 338, 79, { arrow: true });
    s += K.box(340, 34, 96, 90, 'Outcome:\naverage\nwaiting time', { c: 5, size: 12 });
    s += K.text(220, 176, 'Change the variables, then watch what happens', { size: 12, cls: 't-mut' });
    return K.svg(440, 190, s, { title: 'A simulation changes variables in a computer model to see the outcome' });
  });

  D.register('xi6.primary-secondary', () => {
    let s = '';
    const panel = (x, c, title, sub, chips, foot) => {
      let o = K.rect(x, 4, 212, 218, { c, r: 12 });
      o += K.text(x + 106, 28, title, { size: 15, w: 'b' });
      o += K.text(x + 106, 48, sub, { size: 12 });
      chips.forEach((t, i) => {
        o += K.box(x + 5 + (i % 2) * 103, 84 + Math.floor(i / 2) * 44, 99, 36, t, { c: 6, size: 11, r: 8 });
      });
      o += K.rect(x + 14, 184, 184, 28, { c: 7, r: 14 });
      o += K.text(x + 106, 198, foot, { size: 12, w: 'b', vmid: true });
      return o;
    };
    s += panel(4, 0, 'Primary Data', 'Collected first-hand\nby the researcher', ['Interviews', 'Surveys', 'Observations', 'Experiments'], 'Direct collection');
    s += panel(224, 1, 'Secondary Data', 'Already collected\nby someone else', ['Books, articles', 'Official reports', 'Web statistics', 'Online databases'], 'Existing archives');
    return K.svg(440, 228, s, { title: 'Primary data sources versus secondary data sources' });
  });

  D.register('xi6.approach-steps', () => {
    let s = '';
    const st = [
      'Define the research question clearly',
      'Decide the type of data needed',
      'Select suitable methods',
      'Choose the sample or target group',
      'Prepare tools: forms, questions, sheets',
      'Collect the data carefully',
      'Store digitally and keep a backup',
      'Follow ethics, respect privacy',
    ];
    const cs = [1, 1, 1, 1, 1, 5, 5, 4];
    const tag = ['PLAN', 'PLAN', 'PLAN', 'PLAN', 'PLAN', 'DO', 'DO', 'ALWAYS'];
    st.forEach((t, i) => {
      const y = 6 + i * 42;
      s += K.rect(4, y, 432, 34, { c: cs[i], r: 8 });
      s += K.circle(24, y + 17, 12, { c: 7 }) + K.text(24, y + 17, String(i + 1), { size: 12, w: 'b', vmid: true });
      s += K.text(46, y + 17, t, { size: 13, anchor: 'start', vmid: true });
      s += K.text(428, y + 17, tag[i], { size: 11, anchor: 'end', vmid: true, w: 'b', cls: 't-mut' });
    });
    return K.svg(440, 344, s, { title: 'Eight steps of designing a data-collection approach' });
  });

  D.register('xi6.sample', () => {
    let s = '';
    const picks = { 0: [1, 5, 10], 1: [3, 8, 12], 2: [0, 6, 11] };
    s += K.text(220, 18, 'Population: all Class XI students', { size: 13, w: 'b' });
    ['A', 'B', 'C'].forEach((sec, r) => {
      const y = 48 + r * 36;
      s += K.text(14, y, 'Sec ' + sec, { size: 12, anchor: 'start', vmid: true, cls: 't-mut' });
      for (let i = 0; i < 14; i++) {
        const x = 78 + i * 26;
        const on = picks[r].indexOf(i) >= 0;
        s += K.circle(x, y, 9, { c: on ? 4 : 6, s: on ? 's-acc' : null });
        if (on) s += K.circle(x, y, 3, { cls: 'f-ink' });
      }
    });
    s += K.circle(40, 170, 8, { c: 4, s: 's-acc' }) + K.text(56, 170, '= selected in the sample', { size: 12, anchor: 'start', vmid: true });
    s += K.circle(240, 170, 8, { c: 6 }) + K.text(256, 170, '= not selected', { size: 12, anchor: 'start', vmid: true });
    s += K.rect(4, 190, 432, 44, { c: 5, r: 10 });
    s += K.text(220, 205, 'A good sample represents the whole group:', { size: 12, vmid: true, w: 'b' });
    s += K.text(220, 223, 'different sections, different phone habits (30 to 50 students)', { size: 12, vmid: true });
    return K.svg(440, 244, s, { title: 'A sample taken from every section represents the whole population' });
  });

  D.register('xi6.tools-map', () => {
    let s = '';
    const cards = [
      ['Spreadsheets', 'Excel, Google Sheets,\nApple Numbers', 'Organize, calculate,\nsort, filter, chart', 5],
      ['Presentations', 'PowerPoint, Google Slides,\nCanva, Gamma', 'Explain findings\nto an audience', 1],
      ['Infographics', 'Canva, Adobe Express,\nPower BI, Tableau', 'Show the main idea\nquickly', 4],
      ['Reports', 'Word, Google Docs,\nNotion, Canva Docs', 'Full structured study\nwith conclusions', 2],
    ];
    cards.forEach(([t, tools, use, c], i) => {
      const x = 4 + (i % 2) * 220;
      const y = 4 + Math.floor(i / 2) * 150;
      s += K.rect(x, y, 212, 142, { c, r: 12 });
      s += K.text(x + 106, y + 24, t, { size: 15, w: 'b' });
      s += K.text(x + 106, y + 52, tools, { size: 12 });
      s += K.line(x + 20, y + 80, x + 192, y + 80, { cls: 's-mut', w: 1 });
      s += K.text(x + 106, y + 102, use, { size: 12, w: 'b', cls: 't-acc' });
    });
    return K.svg(440, 304, s, { title: 'Digital tools for presenting data: spreadsheets, presentations, infographics and reports' });
  });

  D.register('xi6.spreadsheet', () => {
    let s = '';
    const cw = [22, 54, 60, 56, 108, 70, 62];
    const hdr = ['', 'No.', 'Phone hrs', 'Study use', 'Main activity', 'Distracted', 'Study hrs'];
    const rows = [
      ['1', '3', 'Yes', 'YouTube lectures', 'Sometimes', '2'],
      ['2', '5', 'No', 'Social media', 'Yes', '1'],
      ['3', '2', 'Yes', 'Searching notes', 'No', '3'],
      ['Total', '10', '', '', '', '6'],
      ['Average', '3.33', '', '', '', '2'],
    ];
    s += K.rect(4, 4, 432, 28, { c: 6, r: 6 });
    s += K.text(18, 18, 'fx', { size: 13, w: 'b', vmid: true, cls: 't-acc' });
    s += K.text(48, 18, '=AVERAGE(B2:B4)', { size: 13, anchor: 'start', vmid: true });
    s += K.text(430, 18, 'result: 3.33', { size: 12, anchor: 'end', vmid: true, cls: 't-mut' });
    const letters = ['', 'A', 'B', 'C', 'D', 'E', 'F'];
    let x = 4;
    const y0 = 42;
    const rh = 28;
    cw.forEach((w, j) => {
      s += K.rect(x, y0, w, 20, { c: 6, r: 0, cls: 'cell' }) + K.text(x + w / 2, y0 + 10, letters[j], { size: 11, vmid: true, cls: 't-mut' });
      x += w;
    });
    const all = [hdr].concat(rows.map((r) => [''].concat(r)));
    all.forEach((r, i) => {
      x = 4;
      cw.forEach((w, j) => {
        const isHead = i === 0;
        const isSum = i >= 4;
        const c = isHead ? 1 : isSum ? 4 : j === 0 ? 6 : null;
        let val = r[j];
        if (j === 0) val = String(i + 1);
        s += K.rect(x, y0 + 20 + i * rh, w, rh, { c, r: 0, cls: 'cell' });
        s += K.text(x + w / 2, y0 + 20 + i * rh + rh / 2, val || '', { size: isHead ? 11 : 12, vmid: true, w: isHead || isSum ? 'b' : '' });
        x += w;
      });
    });
    return K.svg(440, 42 + 20 + 6 * rh + 8, s, { title: 'Spreadsheet with survey rows, totals and an AVERAGE formula' });
  });

  D.register('xi6.bar-chart', (args) => {
    args = args || {};
    const data = args.data || [['Under 1 hr', 4], ['1-3 hrs', 12], ['3-5 hrs', 18], ['Over 5 hrs', 6]];
    const x0 = 56;
    const y0 = 230;
    const top = 50;
    const max = 20;
    const sc = (y0 - top) / max;
    let s = '';
    s += K.text(228, 18, 'Daily mobile phone use of 40 students', { size: 14, w: 'b' });
    s += K.text(228, 36, 'sample data', { size: 11, cls: 't-mut' });
    for (let v = 0; v <= max; v += 5) {
      const y = y0 - v * sc;
      s += K.line(x0, y, 420, y, { cls: 's-mut', w: v === 0 ? 1.8 : 0.8, dash: v === 0 ? '' : '3 4' });
      s += K.text(x0 - 8, y, String(v), { size: 12, anchor: 'end', vmid: true, cls: 't-mut' });
    }
    s += K.line(x0, y0, x0, top - 4, { cls: 's-mut', w: 1.8 });
    s += K.text(14, 140, 'Students', { size: 12, rot: -90, cls: 't-mut' });
    const bw = 58;
    const gap = (364 - bw * data.length) / data.length;
    data.forEach(([l, v], i) => {
      const x = x0 + gap / 2 + i * (bw + gap);
      const h = v * sc;
      s += K.rect(x, y0 - h, bw, h, { c: [1, 0, 5, 4][i % 4], r: 4 });
      s += K.text(x + bw / 2, y0 - h + 18, String(v), { size: 14, w: 'b' });
      s += K.text(x + bw / 2, y0 + 17, l, { size: 12 });
    });
    s += K.text(228, 268, 'Daily phone use (hours)', { size: 12, cls: 't-mut' });
    return K.svg(440, 278, s, { title: 'Bar chart of daily mobile phone use: 4, 12, 18 and 6 students' });
  });

  D.register('xi6.pie-chart', (args) => {
    args = args || {};
    const data = args.data || [['Study', 14], ['Social media', 12], ['Gaming', 6], ['Entertainment', 4], ['Communication', 4]];
    const total = data.reduce((a, d) => a + d[1], 0);
    const cx = 108;
    const cy = 128;
    const r = 88;
    let s = '';
    s += K.text(220, 16, 'Main purpose of phone use (40 students, sample data)', { size: 12, w: 'b' });
    let a0 = -Math.PI / 2;
    data.forEach(([l, v], i) => {
      const a1 = a0 + (v / total) * Math.PI * 2;
      const x1 = cx + r * Math.cos(a0);
      const y1 = cy + r * Math.sin(a0);
      const x2 = cx + r * Math.cos(a1);
      const y2 = cy + r * Math.sin(a1);
      const large = a1 - a0 > Math.PI ? 1 : 0;
      s += K.path('M' + cx + ' ' + cy + ' L' + x1.toFixed(1) + ' ' + y1.toFixed(1) + ' A' + r + ' ' + r + ' 0 ' + large + ' 1 ' + x2.toFixed(1) + ' ' + y2.toFixed(1) + ' Z', { c: [1, 3, 5, 4, 2][i % 5] });
      const am = (a0 + a1) / 2;
      s += K.text(cx + r * 0.62 * Math.cos(am), cy + r * 0.62 * Math.sin(am), Math.round((v / total) * 100) + '%', { size: 13, w: 'b', vmid: true });
      const ly = 62 + i * 36;
      s += K.rect(222, ly - 10, 20, 20, { c: [1, 3, 5, 4, 2][i % 5], r: 4 });
      s += K.text(252, ly, l, { size: 13, anchor: 'start', vmid: true, w: 'b' });
      s += K.text(430, ly, v + ' students', { size: 12, anchor: 'end', vmid: true, cls: 't-mut' });
      a0 = a1;
    });
    s += K.line(222, 232, 430, 232, { cls: 's-mut', w: 1 });
    s += K.text(252, 250, 'Total', { size: 13, anchor: 'start', vmid: true, w: 'b' });
    s += K.text(430, 250, total + ' students = 100%', { size: 12, anchor: 'end', vmid: true, w: 'b' });
    return K.svg(440, 270, s, { title: 'Pie chart of the main purpose of mobile phone use' });
  });

  D.register('xi6.line-graph', (args) => {
    args = args || {};
    const data = args.data || [['Wk 1', 2.5], ['Wk 2', 3.0], ['Wk 3', 3.4], ['Wk 4', 3.2], ['Wk 5', 3.9], ['Wk 6', 3.6]];
    const x0 = 56;
    const y0 = 220;
    const top = 50;
    const max = 5;
    const sc = (y0 - top) / max;
    let s = '';
    s += K.text(228, 18, 'Average daily phone use per week', { size: 14, w: 'b' });
    s += K.text(228, 36, 'sample data, in hours', { size: 11, cls: 't-mut' });
    for (let v = 0; v <= max; v++) {
      const y = y0 - v * sc;
      s += K.line(x0, y, 424, y, { cls: 's-mut', w: v === 0 ? 1.8 : 0.8, dash: v === 0 ? '' : '3 4' });
      s += K.text(x0 - 8, y, String(v), { size: 12, anchor: 'end', vmid: true, cls: 't-mut' });
    }
    s += K.line(x0, y0, x0, top - 4, { cls: 's-mut', w: 1.8 });
    s += K.text(14, 135, 'Hours', { size: 12, rot: -90, cls: 't-mut' });
    const step = (424 - x0 - 30) / (data.length - 1);
    const pts = data.map(([l, v], i) => [x0 + 20 + i * step, y0 - v * sc]);
    s += K.polyline(pts, { s: 's-brand', w: 3 });
    data.forEach(([l, v], i) => {
      s += K.circle(pts[i][0], pts[i][1], 5, { c: 4 });
      s += K.text(pts[i][0], pts[i][1] - 12, String(v), { size: 12, w: 'b' });
      s += K.text(pts[i][0], y0 + 17, l, { size: 12 });
    });
    s += K.text(228, 262, 'Time (weeks)', { size: 12, cls: 't-mut' });
    return K.svg(440, 272, s, { title: 'Line graph showing average daily phone use over six weeks' });
  });

  D.register('xi6.chart-chooser', () => {
    let s = '';
    const rows = [
      ['Table', 'Exact values', 0],
      ['Bar chart', 'Compare categories', 1],
      ['Line graph', 'Show trends over time', 2],
      ['Pie chart', 'Parts of a whole', 3],
      ['Infographic', 'Summarize key findings quickly', 4],
    ];
    rows.forEach(([n, u, i], r) => {
      const y = 6 + r * 56;
      s += K.rect(4, y, 432, 48, { c: r % 2 ? 6 : 1, r: 10 });
      const ix = 14;
      const iy = y + 6;
      if (i === 0) {
        s += K.grid(ix, iy + 4, 18, 9, [[1, 2, 3], [4, 5, 6], [7, 8, 9]], { size: 11 }).replace(/<text[^>]*>.*?<\/text>/g, '');
      } else if (i === 1) {
        [12, 26, 18, 32].forEach((h, k) => (s += K.rect(ix + 4 + k * 12, iy + 36 - h, 9, h, { c: 1, r: 1 })));
      } else if (i === 2) {
        s += K.polyline([[ix + 2, iy + 30], [ix + 14, iy + 20], [ix + 26, iy + 24], [ix + 40, iy + 6]], { s: 's-brand', w: 2.5 });
      } else if (i === 3) {
        s += K.circle(ix + 22, iy + 20, 18, { c: 3 });
        s += K.path('M' + (ix + 22) + ' ' + (iy + 20) + ' L' + (ix + 22) + ' ' + (iy + 2) + ' A18 18 0 0 1 ' + (ix + 40) + ' ' + (iy + 20) + ' Z', { c: 1 });
      } else {
        s += K.rect(ix + 2, iy + 2, 40, 10, { c: 4, r: 2 }) + K.rect(ix + 2, iy + 16, 18, 22, { c: 5, r: 2 }) + K.circle(ix + 33, iy + 28, 10, { c: 2 });
      }
      s += K.text(72, y + 17, n, { size: 14, anchor: 'start', w: 'b', vmid: true });
      s += K.text(72, y + 35, u, { size: 12, anchor: 'start', vmid: true, cls: 't-mut' });
    });
    return K.svg(440, 292, s, { title: 'Which visual to use: table, bar chart, line graph, pie chart, infographic' });
  });

  D.register('xi6.infographic', () => {
    let s = '';
    s += K.rect(8, 6, 290, 372, { c: null, r: 14 });
    s += K.rect(14, 12, 278, 46, { c: 1, r: 10 });
    s += K.text(153, 31, 'Mobile Phones & Study Habits', { size: 14, w: 'b' });
    s += K.text(153, 48, 'Class XI survey, 40 students', { size: 11, cls: 't-mut' });
    [['40', 'students\nsurveyed'], ['3-5 h', 'most common\ndaily use'], ['35%', 'use phone\nfor study']].forEach(([n, l], i) => {
      const x = 14 + i * 95;
      s += K.rect(x, 66, 88, 62, { c: [0, 4, 5][i], r: 8 });
      s += K.text(x + 44, 87, n, { size: 18, w: 'b' });
      s += K.text(x + 44, 105, l, { size: 11 });
    });
    s += K.rect(14, 136, 130, 100, { c: 6, r: 8 });
    [18, 48, 72, 30].forEach((h, k) => (s += K.rect(26 + k * 28, 224 - h, 20, h, { c: [1, 0, 5, 4][k], r: 2 })));
    s += K.rect(152, 136, 140, 100, { c: 6, r: 8 });
    s += K.circle(222, 186, 38, { c: 1 });
    s += K.path('M222 186 L222 148 A38 38 0 0 1 256 203 Z', { c: 3 });
    s += K.path('M222 186 L256 203 A38 38 0 0 1 195 218 Z', { c: 5 });
    s += K.rect(14, 244, 278, 38, { c: 4, r: 8 });
    s += K.text(153, 263, 'Key finding: most use phones 3-5 hours daily', { size: 12, vmid: true, w: 'b' });
    s += K.rect(14, 290, 278, 52, { c: 5, r: 8 });
    s += K.text(153, 306, 'Conclusion: phones help learning', { size: 12, vmid: true, w: 'b' });
    s += K.text(153, 324, 'when used wisely. Turn off notifications.', { size: 12, vmid: true });
    s += K.text(153, 362, 'Source: class survey + online report', { size: 11, vmid: true, cls: 't-mut' });
    const notes = [['1  Clear title', 35], ['2  Key numbers', 97], ['3  Visuals', 186], ['4  Main finding', 263], ['5  Conclusion', 316], ['6  Sources', 362]];
    notes.forEach(([t, y]) => {
      s += K.line(300, y, 318, y, { cls: 's-mut', w: 1.4 });
      s += K.text(322, y, t, { size: 12, anchor: 'start', vmid: true, w: 'b' });
    });
    return K.svg(440, 386, s, { title: 'Layout sketch of an infographic: title, key numbers, charts, finding, conclusion, source' });
  });

  D.register('xi6.scenario', () => {
    let s = '';
    s += K.rect(8, 10, 150, 66, { c: 5, r: 14 });
    s += K.text(83, 43, '"Phones help me\nlearn better"', { size: 12, vmid: true });
    s += K.rect(282, 10, 150, 66, { c: 3, r: 14 });
    s += K.text(357, 43, '"Phones waste time and\nreduce concentration"', { size: 12, vmid: true });
    s += K.rect(184, 28, 72, 112, { c: 6, r: 12 });
    s += K.rect(192, 40, 56, 74, { c: 1, r: 4 });
    s += K.circle(220, 127, 5, { c: 6 });
    s += K.line(158, 43, 184, 70, { cls: 's-mut', dash: '4 3' });
    s += K.line(282, 43, 256, 70, { cls: 's-mut', dash: '4 3' });
    s += K.text(220, 82, 'Phone', { size: 12, w: 'b' });
    s += K.line(220, 142, 220, 170, { arrow: true });
    s += K.rect(20, 172, 400, 52, { c: 4, r: 12 });
    s += K.text(220, 189, 'Research question', { size: 12, w: 'b', cls: 't-acc', vmid: true });
    s += K.text(220, 208, 'How does daily mobile phone use affect study habits?', { size: 12, vmid: true });
    return K.svg(440, 232, s, { title: 'Two opinions about phones lead to the research question' });
  });

  D.register('xi6.case-steps', (args) => {
    args = args || {};
    const part = args.part || 0;
    const names = [
      'Perform advanced\nsearches', 'Identify data types', 'Select collection\nmethods', 'Prepare the survey', 'Choose the sample',
      'Collect primary data', 'Use secondary data', 'Organize data in a\nspreadsheet', 'Create charts and\ngraphs', 'Analyze the results',
      'Write the conclusion', 'Recommendations',
    ];
    const col = [1, 0, 0, 0, 0, 5, 5, 4, 4, 4, 2, 2];
    const w = 124;
    const h = 46;
    const cxs = [8, 156, 304];
    const ys = [12, 80, 148, 216];
    const pos = names.map((_, i) => {
      const r = Math.floor(i / 3);
      const k = i % 3;
      return [cxs[r % 2 ? 2 - k : k], ys[r]];
    });
    let s = '';
    names.forEach((n, i) => {
      if (i === 11) return;
      const [x, y] = pos[i];
      const [x2, y2] = pos[i + 1];
      if (y === y2) {
        const dir = x2 > x ? 1 : -1;
        const a = dir > 0 ? x + w + 1 : x - 1;
        s += K.line(a, y + h / 2, dir > 0 ? x2 - 1 : x2 + w + 1, y2 + h / 2, { arrow: true, w: 1.4 });
      } else {
        s += K.line(x + w / 2, y + h + 1, x2 + w / 2, y2 - 1, { arrow: true, w: 1.4 });
      }
    });
    names.forEach((n, i) => {
      const on = !part || (part === 1 ? i < 5 : i >= 5);
      const [x, y] = pos[i];
      s += K.rect(x, y, w, h, { c: on ? col[i] : 6, r: 10 });
      s += K.text(x + w / 2, y + h / 2, n, { size: 12, vmid: true, cls: on ? '' : 't-mut' });
      s += K.circle(x, y, 11, { c: 7 });
      s += K.text(x, y, String(i + 1), { size: 11, w: 'b', vmid: true });
    });
    const lg = [['Search', 1], ['Plan', 0], ['Collect', 5], ['Analyze', 4], ['Conclude', 2]];
    let lx = 8;
    lg.forEach(([t, c]) => {
      s += K.rect(lx, 280, 16, 16, { c, r: 4 });
      s += K.text(lx + 22, 288, t, { size: 12, anchor: 'start', vmid: true });
      lx += 22 + t.length * 7 + 18;
    });
    return K.svg(440, 308, s, { title: 'Twelve methodology steps of the digital inquiry case study' });
  });

  D.register('xi6.artefact-structure', () => {
    let s = '';
    const secs = ['Title', 'Research Question', 'Introduction', 'Method of Data Collection', 'Primary Data Findings', 'Secondary Data Summary', 'Charts and Graphs', 'Conclusion', 'Recommendations', 'References'];
    const cs = [1, 1, 1, 0, 5, 5, 4, 2, 2, 6];
    s += K.rect(60, 4, 320, 438, { c: null, r: 10 });
    secs.forEach((t, i) => {
      const y = 14 + i * 42;
      s += K.rect(76, y, 288, 34, { c: cs[i], r: 8 });
      s += K.circle(96, y + 17, 11, { c: 7 }) + K.text(96, y + 17, String(i + 1), { size: 12, w: 'b', vmid: true });
      s += K.text(118, y + 17, t, { size: 13, anchor: 'start', vmid: true });
    });
    return K.svg(440, 446, s, { title: 'Ten sections of a digital artefact: from title to references' });
  });

  D.register('xi6.artefact-options', () => {
    let s = '';
    const o = [
      ['Report', 'Structured\ndocument', 2],
      ['Presentation', 'Slides for\nan audience', 1],
      ['Infographic', 'Quick visual\nsummary', 4],
      ['Dashboard', 'Interactive\ncharts, filters', 5],
    ];
    o.forEach(([t, d, c], i) => {
      const x = 4 + i * 110;
      s += K.rect(x, 8, 102, 104, { c, r: 12 });
      s += K.text(x + 51, 30, t, { size: 13, w: 'b' });
      s += K.text(x + 51, 56, d, { size: 12 });
      s += K.line(x + 51, 112, 220, 150, { cls: 's-mut', dash: '4 3' });
    });
    s += K.box(100, 150, 240, 44, 'Digital artefact:\nanswers the research question', { c: 7, size: 12, bold: true });
    return K.svg(440, 206, s, { title: 'Four digital artefact options that answer a research question' });
  });
})();
