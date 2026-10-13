const BOOKS = ["xi", "xii"];
const store = { xi: null, xii: null };
const PROGRESS_KEY = "cs-cheat-progress-v1";
const RATE_KEY = "cs-cheat-rate";

const LABELS = {
  def: "Definition — write this on the paper",
  tip: "Yaad rakho",
  exam: "Paper mein",
  warn: "Dhoka",
  answer: "Jawab"
};

const MODE_LABEL = {
  teach: "Teach",
  checkpoint: "Checkpoint",
  blitz: "Golden blitz",
  recap: "Recap",
  mock: "Mock",
  mark: "Mark",
  repair: "Repair"
};

let speaking = false;
let rate = Number(localStorage.getItem(RATE_KEY) || "0.92");

const $ = (id) => document.getElementById(id);

function progress() {
  try { return JSON.parse(localStorage.getItem(PROGRESS_KEY) || "{}"); }
  catch { return {}; }
}

function setDone(id, done) {
  const data = progress();
  if (done) data[id] = 1;
  else delete data[id];
  localStorage.setItem(PROGRESS_KEY, JSON.stringify(data));
}

function esc(text) {
  return String(text).replace(/[&<>"']/g, (ch) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[ch]));
}

function formatText(text) {
  const parts = String(text).split(/(\\\([\s\S]*?\\\)|\\\[[\s\S]*?\\\])/g);
  return parts.map((part, index) => (index % 2 ? part : esc(part))).join("");
}

function speakable(text) {
  return String(text)
    .replace(/\\\(([\s\S]*?)\\\)|\\\[([\s\S]*?)\\\]/g, (_, a, b) => {
      const tex = a || b || "";
      return " " + tex
        .replace(/\\dfrac|\\frac/g, "")
        .replace(/\\overline\{([^}]+)\}/g, "$1 bar")
        .replace(/\\bar\{([^}]+)\}/g, "$1 bar")
        .replace(/\\cdot/g, " times ")
        .replace(/\\oplus/g, " xor ")
        .replace(/\\log/g, " log ")
        .replace(/\\sum/g, " sum ")
        .replace(/\\rightarrow/g, " to ")
        .replace(/[{}\\]/g, " ")
        .replace(/\^/g, " to the power ")
        + " ";
    })
    .replace(/[★🧠📝⚠]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function cardSpeech(card) {
  const bits = [card.title];
  for (const block of card.blocks || []) {
    if (block.type === "table") {
      bits.push((block.headers || []).join(", "));
      for (const row of block.rows || []) bits.push(row.join(", "));
    } else if (block.text) {
      bits.push(block.text);
    }
  }
  if (card.diagram && DIAGRAMS[card.diagram]) bits.push(DIAGRAMS[card.diagram].caption);
  return speakable(bits.join(". "));
}

function pageSpeech(page) {
  return [page.title, page.subtitle, page.mustLock ? "Must lock. " + page.mustLock : "", ...page.cards.map(cardSpeech)]
    .filter(Boolean)
    .join(". ");
}

function setSpeaking(on) {
  speaking = on;
  document.querySelectorAll("[data-listen]").forEach((button) => {
    button.setAttribute("aria-pressed", on ? "true" : "false");
    button.classList.toggle("speaking", on);
  });
  const main = $("listen-page");
  if (main) main.textContent = on ? "Stop" : "Listen";
}

window.__ttsState = setSpeaking;

function stopSpeech() {
  if (window.AndroidTts) AndroidTts.stop();
  if (window.speechSynthesis) speechSynthesis.cancel();
  setSpeaking(false);
}

function startSpeech(text) {
  stopSpeech();
  if (!text) return;
  if (window.AndroidTts) {
    AndroidTts.speak(text, rate);
    setSpeaking(true);
    return;
  }
  if (!window.speechSynthesis) return;
  const utter = new SpeechSynthesisUtterance(text);
  utter.rate = rate;
  utter.lang = "en-US";
  utter.onend = () => setSpeaking(false);
  utter.onerror = () => setSpeaking(false);
  setSpeaking(true);
  speechSynthesis.speak(utter);
}

async function loadBook(id) {
  if (store[id]) return store[id];
  const response = await fetch("content/" + id + ".json");
  if (!response.ok) throw new Error("Missing " + id);
  store[id] = await response.json();
  return store[id];
}

function route() {
  const hash = location.hash.replace(/^#\/?/, "");
  const [bookId, pageId] = hash.split("/");
  if (!BOOKS.includes(bookId)) return renderHome();
  return renderBook(bookId, pageId);
}

function renderHome() {
  $("rail").classList.add("hidden");
  $("tts-bar").classList.add("hidden");
  $("search").classList.add("hidden");
  $("back").classList.add("hidden");
  const done = progress();
  const counts = BOOKS.map((id) => {
    const book = store[id];
    if (!book) return "";
    const finished = book.pages.filter((page) => done[id + ":" + page.id]).length;
    return finished + " / " + book.pages.length + " days marked";
  });
  $("stage").innerHTML = `
    <section class="home">
      <div class="hero">
        <div class="badge">Version 1.0.0 · offline</div>
        <h1>CS XI &amp; XII cheat-sheet</h1>
        <p>Sindh Curriculum 2026 · 30 days each · Roman Urdu + English. Formulas are set with MathJax, diagrams are SVG, and the layout is Flexbox. Listen uses the phone's voice.</p>
      </div>
      <div class="books">
        <button class="book" data-open="xi">
          <em>Class XI</em>
          <strong>Computer Science XI</strong>
          <span>Computer systems through digital literacy. 45 golden topics.</span>
          <span>${counts[0] || "30 days"}</span>
        </button>
        <button class="book" data-open="xii">
          <em>Class XII</em>
          <strong>Computer Science XII</strong>
          <span>HCI, algorithms, Python, data, machine learning, entrepreneurship. 32 golden topics.</span>
          <span>${counts[1] || "30 days"}</span>
        </button>
      </div>
      <div class="plan">
        <strong>Rozana 3 ghante</strong>
        <p>0–15 min: yesterday's star recap. 15–105: today's cards. 105–135: closed-book drill. 135–180: one 5-mark answer.</p>
      </div>
      <div class="legend">
        <span><b>Definition</b> — write this wording on the paper.</span>
        <span><b>Yaad rakho</b> — the mnemonic.</span>
        <span><b>Paper mein</b> — how the board asks it.</span>
        <span><b>Dhoka</b> — the mistake that costs marks.</span>
      </div>
    </section>`;
  $("stage").querySelectorAll("[data-open]").forEach((button) => {
    button.addEventListener("click", () => {
      const id = button.getAttribute("data-open");
      const book = store[id];
      const first = book && book.pages[0] ? book.pages[0].id : "p03";
      location.hash = "#/" + id + "/" + first;
    });
  });
}

function renderTable(block) {
  const head = `<div class="flex-tr head">${block.headers.map((cell) => `<div class="flex-td">${formatText(cell)}</div>`).join("")}</div>`;
  const rows = (block.rows || []).map((row) => `<div class="flex-tr">${row.map((cell) => `<div class="flex-td">${formatText(cell)}</div>`).join("")}</div>`).join("");
  return `<div class="flex-table">${head}${rows}</div>`;
}

function renderBlock(block) {
  if (block.type === "table") return renderTable(block);
  if (block.type === "code") return `<pre class="code">${esc(block.text)}</pre>`;
  if (LABELS[block.type]) {
    return `<div class="block ${block.type}"><span class="label">${LABELS[block.type]}</span><span>${formatText(block.text)}</span></div>`;
  }
  return `<p class="block">${formatText(block.text)}</p>`;
}

function renderFigure(id) {
  const figure = DIAGRAMS[id];
  if (!figure) return "";
  return `<figure class="figure">${figure.svg}<figcaption>${esc(figure.caption)}</figcaption></figure>`;
}

function whenMathJax() {
  if (window.__mathJaxReady) return window.__mathJaxReady;
  window.__mathJaxReady = new Promise((resolve) => {
    const started = Date.now();
    const timer = setInterval(() => {
      const startup = window.MathJax && MathJax.startup && MathJax.startup.promise;
      if (startup) {
        clearInterval(timer);
        MathJax.startup.promise.then(() => resolve(true)).catch(() => resolve(false));
      } else if (Date.now() - started > 8000) {
        clearInterval(timer);
        resolve(false);
      }
    }, 40);
  });
  return window.__mathJaxReady;
}

async function typeset(node) {
  const ready = await whenMathJax();
  if (!ready || !window.MathJax || !MathJax.typesetPromise) return;
  try {
    if (MathJax.typesetClear) MathJax.typesetClear([node]);
    await MathJax.typesetPromise([node]);
  } catch (error) {
    console.warn(error);
  }
}

async function renderBook(bookId, pageId) {
  const book = await loadBook(bookId);
  const query = ($("search").value || "").trim().toLowerCase();
  let page = book.pages.find((item) => item.id === pageId) || book.pages[0];
  $("rail").classList.remove("hidden");
  $("tts-bar").classList.remove("hidden");
  $("search").classList.remove("hidden");
  $("back").classList.remove("hidden");
  const done = progress();
  $("rail").innerHTML = book.pages.map((item) => {
    const hay = (item.day + " " + item.title + " " + item.chapter).toLowerCase();
    if (query && !hay.includes(query) && item.id !== page.id) return "";
    const active = item.id === page.id ? " active" : "";
    const finished = done[bookId + ":" + item.id] ? " done" : "";
    return `<button class="day-btn${active}${finished}" data-page="${item.id}">
      <small>Day ${item.day} · ${MODE_LABEL[item.mode] || item.mode}</small>
      <strong>${esc(item.title)}</strong>
    </button>`;
  }).join("") || `<p class="empty">No day matches.</p>`;

  const cards = page.cards.filter((card) => {
    if (!query) return true;
    const blob = (card.title + " " + JSON.stringify(card.blocks)).toLowerCase();
    return blob.includes(query);
  });
  const key = bookId + ":" + page.id;
  $("stage").innerHTML = `
    <article class="reader">
      <header class="day-head">
        <div class="kicker">
          <span class="badge">${esc(book.short)} · Day ${esc(page.day)}</span>
          <span class="badge">${esc(MODE_LABEL[page.mode] || "")}</span>
          ${page.mustLock ? `<span class="badge gold">Must lock</span>` : ""}
        </div>
        <h1>${esc(page.title)}</h1>
        <p>${esc(page.chapter || "")}${page.subtitle ? " · " + esc(page.subtitle) : ""}</p>
        ${page.mustLock ? `<p><strong>Must lock:</strong> ${esc(page.mustLock)}</p>` : ""}
        <div class="head-row">
          <label class="check"><input type="checkbox" id="done" ${done[key] ? "checked" : ""}/> Mark day done</label>
        </div>
      </header>
      <div class="cards" id="cards">
        ${cards.map((card, index) => `
          <section class="card ${card.kind}">
            <div class="card-head">
              <h2>${esc(card.title || "Notes")}</h2>
              <div class="card-tools">
                ${card.golden ? `<span class="golden">Golden</span>` : ""}
                <button class="mini" data-card="${index}">Listen</button>
              </div>
            </div>
            ${card.diagram ? renderFigure(card.diagram) : ""}
            ${(card.blocks || []).map(renderBlock).join("")}
          </section>`).join("") || `<p class="empty">No cards match this search.</p>`}
      </div>
    </article>`;

  $("rail").querySelectorAll("[data-page]").forEach((button) => {
    button.addEventListener("click", () => {
      location.hash = "#/" + bookId + "/" + button.getAttribute("data-page");
    });
  });
  const active = $("rail").querySelector(".active");
  if (active) active.scrollIntoView({ block: "nearest", inline: "nearest" });
  $("done").addEventListener("change", (event) => {
    setDone(key, event.target.checked);
    renderBook(bookId, page.id);
  });
  $("stage").querySelectorAll("[data-card]").forEach((button) => {
    button.addEventListener("click", () => startSpeech(cardSpeech(cards[Number(button.getAttribute("data-card"))])));
  });
  $("listen-page").onclick = () => {
    if (speaking) stopSpeech();
    else startSpeech(pageSpeech(page));
  };
  const index = book.pages.findIndex((item) => item.id === page.id);
  $("prev").disabled = index <= 0;
  $("next").disabled = index >= book.pages.length - 1;
  $("prev").onclick = () => { if (index > 0) location.hash = "#/" + bookId + "/" + book.pages[index - 1].id; };
  $("next").onclick = () => { if (index < book.pages.length - 1) location.hash = "#/" + bookId + "/" + book.pages[index + 1].id; };
  await typeset($("cards"));
}

async function boot() {
  await Promise.all(BOOKS.map(loadBook));
  $("rate").value = String(rate);
  $("rate").addEventListener("input", () => {
    rate = Number($("rate").value);
    localStorage.setItem(RATE_KEY, String(rate));
    if (window.AndroidTts) AndroidTts.setRate(rate);
  });
  $("back").addEventListener("click", () => {
    if (location.hash.split("/").length > 2) location.hash = "#/";
    else history.back();
  });
  $("stop").addEventListener("click", stopSpeech);
  $("search").addEventListener("input", () => route());
  window.addEventListener("hashchange", () => {
    stopSpeech();
    route();
  });
  route();
}

boot().catch((error) => {
  $("stage").innerHTML = `<p class="empty">Could not open the booklet. ${esc(error.message)}</p>`;
});
