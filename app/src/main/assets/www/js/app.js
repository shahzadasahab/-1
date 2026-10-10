(function () {
  const view = document.getElementById("view");
  const backBtn = document.getElementById("backBtn");
  const scriptBtn = document.getElementById("scriptBtn");
  const player = document.getElementById("player");
  const playerTitle = document.getElementById("playerTitle");
  const playerState = document.getElementById("playerState");
  const listenBtn = document.getElementById("listenBtn");
  const pdfBtn = document.getElementById("pdfBtn");
  const barTitle = document.getElementById("barTitle");
  const barSub = document.getElementById("barSub");

  const APP = window.CS_APP;
  let route = { page: "home" };
  let speaking = false;
  let showScript = false;

  function nativeBridge() {
    return window.AndroidLecture || null;
  }

  function topicCount(book) {
    return book.chapters.reduce(function (n, ch) { return n + ch.topics.length; }, 0);
  }

  function findBook(id) {
    return APP.books.find(function (b) { return b.id === id; });
  }

  function findTopic(id) {
    for (let i = 0; i < APP.books.length; i++) {
      const book = APP.books[i];
      for (let j = 0; j < book.chapters.length; j++) {
        const chapter = book.chapters[j];
        for (let k = 0; k < chapter.topics.length; k++) {
          if (chapter.topics[k].id === id) {
            return { book: book, chapter: chapter, topic: chapter.topics[k] };
          }
        }
      }
    }
    return null;
  }

  function parseHash() {
    const hash = (location.hash || "#/home").replace(/^#/, "");
    const parts = hash.split("/").filter(Boolean);
    if (parts[0] === "book" && parts[1]) return { page: "book", bookId: parts[1] };
    if (parts[0] === "topic" && parts[1]) return { page: "topic", topicId: parts[1] };
    return { page: "home" };
  }

  function go(hash) {
    location.hash = hash;
  }

  function typeset() {
    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise([view]).catch(function () {});
    }
  }

  function renderHome() {
    barTitle.textContent = APP.title;
    barSub.textContent = APP.subtitle;
    backBtn.classList.add("hidden");
    scriptBtn.classList.add("hidden");
    player.classList.add("hidden");
    const cards = APP.books.map(function (book) {
      return (
        '<button class="book-card" style="background:' + book.accent + '" data-go="#/book/' + book.id + '">' +
          "<small>" + escapeHtml(book.badge) + "</small>" +
          "<h2>" + escapeHtml(book.title) + "</h2>" +
          "<p>" + escapeHtml(book.subtitle) + "</p>" +
          '<div class="count">' + topicCount(book) + " embedded topics · " + book.chapters.length + " units</div>" +
        "</button>"
      );
    }).join("");
    view.innerHTML =
      '<section class="hero">' +
        "<h1>" + escapeHtml(APP.title) + "</h1>" +
        "<p>" + escapeHtml(APP.curriculum) + ". English notes stay on screen. Tap Listen for an Urdu classroom lecture powered by device TTS. Formulas render with embedded MathJax SVG. Layout is Flexbox throughout.</p>" +
        '<div class="badge-row">' +
          '<span class="badge">English text</span>' +
          '<span class="badge">Urdu TTS lectures</span>' +
          '<span class="badge">MathJax SVG</span>' +
          '<span class="badge">Flexbox</span>' +
          '<span class="badge">Offline embedded</span>' +
        "</div>" +
      "</section>" +
      '<section class="book-grid">' + cards + "</section>" +
      '<p class="note">Source PDFs for Class XI, Class XII, and both Q&amp;A books are bundled inside the APK. Open any topic, then Original PDF to see the teacher-edition page.</p>';
  }

  function renderBook(bookId) {
    const book = findBook(bookId);
    if (!book) return renderHome();
    barTitle.textContent = book.title;
    barSub.textContent = book.urTitle;
    backBtn.classList.remove("hidden");
    scriptBtn.classList.add("hidden");
    player.classList.add("hidden");
    const chapters = book.chapters.map(function (ch) {
      const topics = ch.topics.map(function (topic) {
        return (
          '<article class="topic-card" data-go="#/topic/' + topic.id + '">' +
            "<div><h3>" + (topic.golden ? '<span class="star">★ </span>' : "") + escapeHtml(topic.title) + "</h3>" +
            "<span>Pages " + topic.startPage + "–" + topic.endPage + "</span></div>" +
            "<span>Open</span>" +
          "</article>"
        );
      }).join("");
      return (
        '<section class="chapter">' +
          "<header><h2>" + escapeHtml(ch.title) + "</h2><span class='badge'>" + ch.topics.length + "</span></header>" +
          '<div class="topic-list">' + topics + "</div>" +
        "</section>"
      );
    }).join("");
    view.innerHTML =
      '<section class="hero">' +
        "<h1>" + escapeHtml(book.title) + "</h1>" +
        "<p>" + escapeHtml(book.subtitle) + "</p>" +
      "</section>" +
      '<div class="chapter-list">' + chapters + "</div>";
  }

  function renderTopic(topicId) {
    const found = findTopic(topicId);
    if (!found) return renderHome();
    const topic = found.topic;
    const book = found.book;
    barTitle.textContent = topic.title;
    barSub.textContent = found.chapter.title;
    backBtn.classList.remove("hidden");
    scriptBtn.classList.remove("hidden");
    player.classList.remove("hidden");
    playerTitle.textContent = topic.title;
    playerState.textContent = speaking ? "Speaking Urdu lecture…" : "Urdu lecture ready";
    listenBtn.textContent = speaking ? "Stop" : "Listen";
    listenBtn.className = speaking ? "danger" : "gold";
    pdfBtn.dataset.pdf = book.pdf;
    pdfBtn.dataset.page = String(topic.startPage);
    listenBtn.dataset.lecture = topic.urduLecture;
    const script = showScript
      ? '<section class="lecture-panel">' + escapeHtml(topic.urduLecture) + "</section>"
      : "";
    view.innerHTML =
      '<section class="hero">' +
        "<h1>" + (topic.golden ? "★ " : "") + escapeHtml(topic.title) + "</h1>" +
        "<p>" + escapeHtml(found.chapter.title) + " · " + escapeHtml(book.title) + " · pages " +
          topic.startPage + "–" + topic.endPage + "</p>" +
        '<div class="badge-row">' +
          (topic.golden ? '<span class="badge">Golden topic</span>' : "") +
          '<span class="badge">English notes</span>' +
          '<span class="badge">Urdu lecture</span>' +
        "</div>" +
      "</section>" +
      script +
      '<article class="article card" style="padding:16px">' + topic.html + "</article>" +
      '<p class="note">Keep reading the English. The Listen button explains the same idea as a teacher lecture in Urdu. Math is MathJax SVG, not a screenshot.</p>';
    typeset();
  }

  function escapeHtml(text) {
    return String(text || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function render() {
    route = parseHash();
    if (route.page === "book") renderBook(route.bookId);
    else if (route.page === "topic") renderTopic(route.topicId);
    else renderHome();
  }

  function webSpeak(text) {
    if (!window.speechSynthesis) {
      playerState.textContent = "TTS not available in this browser. Showing Urdu script.";
      showScript = true;
      render();
      return;
    }
    window.speechSynthesis.cancel();
    const utter = new SpeechSynthesisUtterance(text);
    const voices = window.speechSynthesis.getVoices();
    const urdu = voices.find(function (v) { return (v.lang || "").toLowerCase().indexOf("ur") === 0; });
    utter.lang = urdu ? urdu.lang : "ur-PK";
    if (urdu) utter.voice = urdu;
    utter.rate = 0.92;
    utter.onstart = function () { setSpeaking(true); };
    utter.onend = function () { setSpeaking(false); };
    utter.onerror = function () { setSpeaking(false); };
    window.speechSynthesis.speak(utter);
    setSpeaking(true);
  }

  function setSpeaking(on) {
    speaking = on;
    playerState.textContent = on ? "Speaking Urdu lecture…" : "Urdu lecture ready";
    listenBtn.textContent = on ? "Stop" : "Listen";
    listenBtn.className = on ? "danger" : "gold";
    player.classList.toggle("speaking", on);
  }

  function stopSpeech() {
    const bridge = nativeBridge();
    if (bridge && bridge.stop) bridge.stop();
    if (window.speechSynthesis) window.speechSynthesis.cancel();
    setSpeaking(false);
  }

  function startSpeech(text) {
    const bridge = nativeBridge();
    if (bridge && bridge.speakUrdu) {
      bridge.speakUrdu(text);
      setSpeaking(true);
      return;
    }
    webSpeak(text);
  }

  document.addEventListener("click", function (event) {
    const goEl = event.target.closest("[data-go]");
    if (goEl) {
      go(goEl.getAttribute("data-go"));
      return;
    }
    if (event.target === backBtn) {
      if (route.page === "topic") {
        const found = findTopic(route.topicId);
        go(found ? "#/book/" + found.book.id : "#/home");
      } else {
        go("#/home");
      }
      return;
    }
    if (event.target === scriptBtn) {
      showScript = !showScript;
      scriptBtn.textContent = showScript ? "Hide script" : "Urdu script";
      render();
      return;
    }
    if (event.target === listenBtn) {
      if (speaking) stopSpeech();
      else startSpeech(listenBtn.dataset.lecture || "");
      return;
    }
    if (event.target === pdfBtn) {
      const bridge = nativeBridge();
      if (bridge && bridge.openPdf) {
        bridge.openPdf(pdfBtn.dataset.pdf, parseInt(pdfBtn.dataset.page || "1", 10));
      } else {
        playerState.textContent = "PDF viewer is available in the Android APK.";
      }
    }
  });

  window.CSCompositeNative = {
    onSpeaking: function (on) { setSpeaking(!!on); },
    onVoiceMessage: function (msg) { playerState.textContent = msg; }
  };

  window.addEventListener("hashchange", render);
  if (window.speechSynthesis) {
    window.speechSynthesis.onvoiceschanged = function () {};
  }
  render();
})();
