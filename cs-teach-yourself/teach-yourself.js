(function () {
  "use strict";

  const synth = window.speechSynthesis;
  let voices = [];

  function loadVoices() {
    voices = synth.getVoices();
    const sel = document.getElementById("tts-voice");
    if (!sel || sel.options.length) return;
    const preferred = voices.filter(
      (v) =>
        v.lang.startsWith("en") ||
        v.lang.startsWith("ur") ||
        v.lang.startsWith("hi")
    );
    (preferred.length ? preferred : voices).forEach((v, i) => {
      const opt = document.createElement("option");
      opt.value = String(i);
      opt.textContent = `${v.name} (${v.lang})`;
      sel.appendChild(opt);
    });
  }

  if (synth.onvoiceschanged !== undefined) {
    synth.onvoiceschanged = loadVoices;
  }
  loadVoices();

  function plainText(el) {
    return (el.innerText || el.textContent || "").replace(/\s+/g, " ").trim();
  }

  function speak(text) {
    if (!text || !synth) return;
    synth.cancel();
    const utter = new SpeechSynthesisUtterance(text);
    const sel = document.getElementById("tts-voice");
    const rate = document.getElementById("tts-rate");
    if (sel && voices[Number(sel.value)]) {
      utter.voice = voices[Number(sel.value)];
    }
    if (rate) utter.rate = Number(rate.value);
    synth.speak(utter);
  }

  document.getElementById("tts-stop")?.addEventListener("click", () => synth.cancel());

  document.querySelectorAll(".tts-read").forEach((btn) => {
    btn.addEventListener("click", () => {
      const sel = btn.getAttribute("data-tts-target");
      const target = sel ? document.querySelector(sel) : btn.closest(".day-card");
      if (target) speak(plainText(target));
    });
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

  const dayLinks = document.querySelectorAll(".nav-day");
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const id = entry.target.id;
        dayLinks.forEach((a) => {
          a.classList.toggle("active", a.getAttribute("href") === `#${id}`);
        });
      });
    },
    { rootMargin: "-20% 0px -60% 0px", threshold: 0 }
  );

  document.querySelectorAll(".day-card").forEach((card) => observer.observe(card));

  if (window.MathJax?.typesetPromise) {
    window.MathJax.typesetPromise().catch(() => {});
  }
})();
