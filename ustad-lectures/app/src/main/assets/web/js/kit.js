/* SVG diagram kit: tiny helpers that emit themed inline SVG strings.
 *
 * Every diagram is a function (args) => string created with K.svg(w, h, inner).
 * Colours come from CSS classes (see .dg in app.css) so diagrams follow light/dark mode.
 *   fill classes   c0..c7  (pastel fills)      stroke classes  s-acc, s-mut, s-red, s-grn
 *   text classes   t-mut, t-acc, t-wht
 * Keep viewBox width <= 480 so text stays readable on a phone; the SVG shrinks to fit.
 */
(function (g) {
  'use strict';

  let uid = 0;
  const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const n = (v) => (Math.round(v * 100) / 100).toString();
  const cls = (...a) => a.filter(Boolean).join(' ');

  function svg(w, h, inner, o) {
    o = o || {};
    const id = 'ar' + ++uid;
    const title = o.title ? '<title>' + esc(o.title) + '</title>' : '';
    return (
      '<svg class="dg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + w + ' ' + h + '" width="' + w +
      '" role="img"' + (o.title ? ' aria-label="' + esc(o.title) + '"' : '') + '>' + title +
      '<defs>' +
      '<marker id="' + id + '" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="mk"/></marker>' +
      '</defs>' +
      inner.split('url(#ARROW)').join('url(#' + id + ')') +
      '</svg>'
    );
  }

  function rect(x, y, w, h, o) {
    o = o || {};
    return (
      '<rect x="' + n(x) + '" y="' + n(y) + '" width="' + n(w) + '" height="' + n(h) + '" rx="' + (o.r == null ? 8 : o.r) +
      '" class="' + cls('shape', o.c != null ? 'c' + o.c : 'c-none', o.s, o.cls) + '"' + (o.dash ? ' stroke-dasharray="' + o.dash + '"' : '') + '/>'
    );
  }

  function text(x, y, str, o) {
    o = o || {};
    const size = o.size || 14;
    const lines = String(str).split('\n');
    const lh = o.lh || size * 1.25;
    const y0 = o.vmid ? y - ((lines.length - 1) * lh) / 2 : y;
    const tsp = lines
      .map((l, i) => '<tspan x="' + n(x) + '" dy="' + (i === 0 ? 0 : n(lh)) + '">' + esc(l) + '</tspan>')
      .join('');
    return (
      '<text x="' + n(x) + '" y="' + n(y0) + '" font-size="' + size + '" text-anchor="' + (o.anchor || 'middle') +
      '" dominant-baseline="' + (o.vmid ? 'central' : 'auto') + '" class="' + cls('tx', o.w === 'b' ? 'tb' : '', o.cls) +
      '"' + (o.rot ? ' transform="rotate(' + o.rot + ' ' + n(x) + ' ' + n(y) + ')"' : '') + '>' + tsp + '</text>'
    );
  }

  function line(x1, y1, x2, y2, o) {
    o = o || {};
    const m =
      (o.arrow === 'both' ? ' marker-start="url(#ARROW)" marker-end="url(#ARROW)"' : '') +
      (o.arrow === true || o.arrow === 'end' ? ' marker-end="url(#ARROW)"' : '') +
      (o.arrow === 'start' ? ' marker-start="url(#ARROW)"' : '');
    return (
      '<line x1="' + n(x1) + '" y1="' + n(y1) + '" x2="' + n(x2) + '" y2="' + n(y2) + '" class="' + cls('ln', o.s, o.cls) + '"' +
      (o.dash ? ' stroke-dasharray="' + o.dash + '"' : '') + (o.w ? ' stroke-width="' + o.w + '"' : '') + m + '/>'
    );
  }

  function path(d, o) {
    o = o || {};
    const m =
      (o.arrow === 'both' ? ' marker-start="url(#ARROW)" marker-end="url(#ARROW)"' : '') +
      (o.arrow === true || o.arrow === 'end' ? ' marker-end="url(#ARROW)"' : '');
    return (
      '<path d="' + d + '" class="' + cls(o.c != null ? 'shape c' + o.c : o.fill ? 'shape ' + o.fill : 'ln', o.s, o.cls) + '"' +
      (o.dash ? ' stroke-dasharray="' + o.dash + '"' : '') + (o.w ? ' stroke-width="' + o.w + '"' : '') + m + '/>'
    );
  }

  function poly(pts, o) {
    o = o || {};
    return (
      '<polygon points="' + pts.map((p) => n(p[0]) + ',' + n(p[1])).join(' ') + '" class="' + cls('shape', o.c != null ? 'c' + o.c : 'c-none', o.s, o.cls) + '"/>'
    );
  }

  function polyline(pts, o) {
    o = o || {};
    const m = o.arrow ? ' marker-end="url(#ARROW)"' : '';
    return (
      '<polyline points="' + pts.map((p) => n(p[0]) + ',' + n(p[1])).join(' ') + '" class="' + cls('ln', o.s, o.cls) + '"' +
      (o.dash ? ' stroke-dasharray="' + o.dash + '"' : '') + (o.w ? ' stroke-width="' + o.w + '"' : '') + m + '/>'
    );
  }

  function circle(cx, cy, r, o) {
    o = o || {};
    return '<circle cx="' + n(cx) + '" cy="' + n(cy) + '" r="' + n(r) + '" class="' + cls('shape', o.c != null ? 'c' + o.c : 'c-none', o.s, o.cls) + '"/>';
  }

  function ellipse(cx, cy, rx, ry, o) {
    o = o || {};
    return '<ellipse cx="' + n(cx) + '" cy="' + n(cy) + '" rx="' + n(rx) + '" ry="' + n(ry) + '" class="' + cls('shape', o.c != null ? 'c' + o.c : 'c-none', o.s, o.cls) + '"/>';
  }

  function dot(x, y, r) {
    return '<circle cx="' + n(x) + '" cy="' + n(y) + '" r="' + (r || 3) + '" class="dot"/>';
  }

  /** rectangle with centred (multi-line) label */
  function box(x, y, w, h, label, o) {
    o = o || {};
    return (
      rect(x, y, w, h, o) +
      text(x + w / 2, y + h / 2, label, { size: o.size || 14, vmid: true, w: o.bold ? 'b' : '', cls: o.tcls })
    );
  }

  function g_(inner, o) {
    o = o || {};
    return '<g' + (o.t ? ' transform="' + o.t + '"' : '') + (o.cls ? ' class="' + o.cls + '"' : '') + '>' + inner + '</g>';
  }

  /** orthogonal wire through points */
  function wire(pts, o) {
    return polyline(pts, o);
  }

  /**
   * Logic gate symbols (ANSI/distinctive shape). Gate body occupies x..x+W, y..y+50.
   * Returns { svg, a:[x,y], b:[x,y], q:[x,y] } with pin coordinates ready for wires.
   */
  function gate(type, x, y, o) {
    o = o || {};
    type = type.toUpperCase();
    const inv = type === 'NAND' || type === 'NOR' || type === 'XNOR' || type === 'NOT';
    let body = '';
    let tipX;
    let aX = x;
    let bX = x;
    const two = type !== 'NOT' && type !== 'BUF';
    const k = 'shape gate ' + (o.c != null ? 'c' + o.c : 'c-none');
    if (type === 'AND' || type === 'NAND') {
      body = '<path d="M' + x + ' ' + y + ' L' + (x + 30) + ' ' + y + ' A25 25 0 0 1 ' + (x + 30) + ' ' + (y + 50) + ' L' + x + ' ' + (y + 50) + ' Z" class="' + k + '"/>';
      tipX = x + 55;
    } else if (type === 'OR' || type === 'NOR' || type === 'XOR' || type === 'XNOR') {
      const xo = type === 'XOR' || type === 'XNOR';
      body =
        '<path d="M' + x + ' ' + y + ' C' + (x + 30) + ' ' + y + ' ' + (x + 48) + ' ' + (y + 10) + ' ' + (x + 58) + ' ' + (y + 25) +
        ' C' + (x + 48) + ' ' + (y + 40) + ' ' + (x + 30) + ' ' + (y + 50) + ' ' + x + ' ' + (y + 50) + ' Q' + (x + 16) + ' ' + (y + 25) + ' ' + x + ' ' + y + ' Z" class="' + k + '"/>';
      if (xo) body += '<path d="M' + (x - 8) + ' ' + y + ' Q' + (x + 8) + ' ' + (y + 25) + ' ' + (x - 8) + ' ' + (y + 50) + '" class="ln"/>';
      tipX = x + 58;
      aX = bX = x + 6.5;
      if (xo) aX = bX = x - 1.5;
    } else {
      body = '<polygon points="' + x + ',' + y + ' ' + x + ',' + (y + 50) + ' ' + (x + 46) + ',' + (y + 25) + '" class="' + k + '"/>';
      tipX = x + 46;
      aX = x;
    }
    let outX = tipX;
    if (inv) {
      body += '<circle cx="' + (tipX + 5) + '" cy="' + (y + 25) + '" r="5" class="shape c-none gate"/>';
      outX = tipX + 10;
    }
    const label = o.label === false ? '' : text(x + (type === 'NOT' || type === 'BUF' ? 14 : 22), y + 25, o.label || type, { size: 11, vmid: true, cls: 't-mut', anchor: 'middle' });
    return {
      svg: body + (o.label ? label : ''),
      a: two ? [aX, y + 14] : [x, y + 25],
      b: two ? [bX, y + 36] : null,
      q: [outX, y + 25],
      w: outX - x,
    };
  }

  /** cell grid helper: returns svg for a rows x cols table of strings */
  function grid(x, y, cw, ch, rows, o) {
    o = o || {};
    let s = '';
    rows.forEach((r, i) => {
      r.forEach((v, j) => {
        const head = o.head && i === 0;
        const c = head ? 'c-head' : o.fills && o.fills[i] && o.fills[i][j] != null ? 'c' + o.fills[i][j] : 'c-none';
        s += '<rect x="' + (x + j * cw) + '" y="' + (y + i * ch) + '" width="' + cw + '" height="' + ch + '" class="shape cell ' + c + '"/>';
        s += text(x + j * cw + cw / 2, y + i * ch + ch / 2, String(v), { size: o.size || 14, vmid: true, w: head ? 'b' : '' });
      });
    });
    return s;
  }

  g.K = { svg, rect, text, line, path, poly, polyline, circle, ellipse, dot, box, g: g_, wire, gate, grid, esc };
})(typeof window !== 'undefined' ? window : globalThis);
