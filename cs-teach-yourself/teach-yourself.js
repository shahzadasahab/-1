(function () {
  "use strict";

  const synth = window.speechSynthesis;
  const isIOS =
    /iPad|iPhone|iPod/.test(navigator.userAgent) ||
    (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
  let voices = [];
  let voiceByUri = new Map();
  let speakQueue = [];
  let speaking = false;

  function loadVoices() {
    if (!synth) return;
    voices = synth.getVoices();
    voiceByUri.clear();
    voices.forEach((v) => voiceByUri.set(v.voiceURI, v));

    const sel = document.getElementById("tts-voice");
    if (!sel || sel.dataset.ready === "1") return;

    const preferred = voices.filter(
      (v) =>
        v.lang.startsWith("en") ||
        v.lang.startsWith("ur") ||
        v.lang.startsWith("hi")
    );
    const list = preferred.length ? preferred : voices;
    list.forEach((v) => {
      const opt = document.createElement("option");
      opt.value = v.voiceURI;
      opt.textContent = `${v.name} (${v.lang})`;
      sel.appendChild(opt);
    });
    sel.dataset.ready = "1";

    if (isIOS && list.length && !sel.value) {
      const en = list.find((v) => v.lang.startsWith("en")) || list[0];
      sel.value = en.voiceURI;
    }
  }

  function primeVoices() {
    loadVoices();
    if (isIOS && synth) {
      synth.cancel();
      const u = new SpeechSynthesisUtterance(" ");
      u.volume = 0;
      synth.speak(u);
      synth.cancel();
    }
  }

  if (synth) {
    if (synth.onvoiceschanged !== undefined) {
      synth.onvoiceschanged = loadVoices;
    }
    loadVoices();
    document.addEventListener(
      "touchstart",
      () => primeVoices(),
      { once: true, passive: true }
    );
    document.addEventListener("click", () => primeVoices(), { once: true });
  }

  function plainText(el) {
    return (el.innerText || el.textContent || "").replace(/\s+/g, " ").trim();
  }

  function chunkText(text, maxLen) {
    if (text.length <= maxLen) return [text];
    const parts = [];
    let rest = text;
    while (rest.length > maxLen) {
      let cut = rest.lastIndexOf(". ", maxLen);
      if (cut < maxLen * 0.4) cut = rest.lastIndexOf(" ", maxLen);
      if (cut < 1) cut = maxLen;
      parts.push(rest.slice(0, cut).trim());
      rest = rest.slice(cut).trim();
    }
    if (rest) parts.push(rest);
    return parts;
  }

  function speakNext() {
    if (!speakQueue.length) {
      speaking = false;
      return;
    }
    speaking = true;
    const text = speakQueue.shift();
    const utter = new SpeechSynthesisUtterance(text);
    const sel = document.getElementById("tts-voice");
    const rate = document.getElementById("tts-rate");
    if (sel?.value && voiceByUri.has(sel.value)) {
      utter.voice = voiceByUri.get(sel.value);
    }
    if (rate) utter.rate = Number(rate.value);
    utter.onend = () => speakNext();
    utter.onerror = () => speakNext();
    synth.speak(utter);
  }

  function speak(text) {
    if (!text || !synth) return;
    synth.cancel();
    speakQueue = chunkText(text, isIOS ? 180 : 400);
    speaking = false;
    speakNext();
  }

  document.getElementById("tts-stop")?.addEventListener("click", () => {
    speakQueue = [];
    synth?.cancel();
    speaking = false;
  });

  document.querySelectorAll(".tts-read").forEach((btn) => {
    const handler = (e) => {
      e.preventDefault();
      primeVoices();
      const sel = btn.getAttribute("data-tts-target");
      const target = sel ? document.querySelector(sel) : btn.closest(".day-card");
      if (target) speak(plainText(target));
    };
    btn.addEventListener("click", handler);
    btn.addEventListener("touchend", handler, { passive: false });
  });

  document.querySelectorAll(".drill-toggle").forEach((btn) => {
    btn.addEventListener("click", () => {
      const panel = btn.closest(".day-card")?.querySelector(".checkpoint-panel");
      if (!panel) return;
      const open = panel.hasAttribute("open");
      if (open) panel.removeAttribute("open");
      else panel.setAttribute("open", "");
      btn.setAttribute("aria-expanded", String(!open));
    });
  });

  function setupMobileDayJump() {
    const nav = document.querySelector(".sidebar");
    const links = nav?.querySelectorAll(".nav-day");
    if (!nav || !links?.length) return;

    let bar = document.querySelector(".mobile-day-jump");
    if (!bar) {
      bar = document.createElement("div");
      bar.className = "mobile-day-jump flex-row";
      bar.innerHTML =
        '<label for="day-jump">Day</label><select id="day-jump" aria-label="Jump to day"></select>';
      nav.parentElement?.insertBefore(bar, nav);
    }

    const select = bar.querySelector("#day-jump");
    if (!select || select.options.length) return;

    links.forEach((a) => {
      const opt = document.createElement("option");
      opt.value = a.getAttribute("href") || "";
      opt.textContent = a.textContent?.trim() || opt.value;
      select.appendChild(opt);
    });

    select.addEventListener("change", () => {
      const id = select.value.replace("#", "");
      const el = document.getElementById(id);
      if (el) {
        el.scrollIntoView({ behavior: "smooth", block: "start" });
        history.replaceState(null, "", select.value);
      }
    });
  }

  setupMobileDayJump();

  const dayLinks = document.querySelectorAll(".nav-day");
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const id = entry.target.id;
        dayLinks.forEach((a) => {
          a.classList.toggle("active", a.getAttribute("href") === `#${id}`);
        });
        const jump = document.getElementById("day-jump");
        if (jump) jump.value = `#${id}`;
      });
    },
    { rootMargin: "-25% 0px -55% 0px", threshold: 0 }
  );

  document.querySelectorAll(".day-card").forEach((card) => observer.observe(card));

  function typesetMath() {
    if (window.MathJax?.typesetPromise) {
      window.MathJax.typesetPromise().catch(() => {});
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", typesetMath);
  } else {
    typesetMath();
  }
  window.addEventListener("load", typesetMath);

  if (isIOS) {
    const hint = document.createElement("p");
    hint.className = "ios-tts-hint";
    hint.textContent =
      "iPhone: tap Listen once; long lessons read in parts. Keep screen on.";
    document.querySelector(".tts-bar")?.appendChild(hint);
  }
})();
