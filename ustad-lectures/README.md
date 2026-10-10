# Ustad Lectures — Teacher's Lecture-wise APK (Urdish TTS)

**Download (v1.0.0 debug):** [UstadLectures-v1.0.0-debug.apk](https://github.com/shahzadasahab/-1/raw/cursor/teacher-lectures-apk-b9d1/ustad-lectures/releases/UstadLectures-v1.0.0-debug.apk)

Lecture-wise Computer Science teaching app for the **Class XI and XII** textbooks. Every lecture is delivered the way
a teacher speaks in a Pakistani classroom:

* **Urdish narration** — descriptive explanation in Urdu script, technical terminology in English.
* **Text-to-Speech (TTS)** — each sentence is split into Urdu and English runs; Android `TextToSpeech` switches between an
  Urdu voice (`ur-PK`) and an English voice (`en-IN`/`en-US`) inside one lecture. The sentence being spoken is highlighted and scrolled into view.
* **MathJax** (bundled, offline, SVG output) for Boolean algebra, Big-O, statistics, neural-network formulas.
* **SVG diagrams** — hand-built, theme-aware inline SVG (logic gates, K-maps, OSI model, ER diagrams, sorting traces,
  data structures, charts ...).
* **Flexbox UI** — app shell, lecture cards, tables, comparisons, term chips, steps and player are all CSS flexbox.
* Per lecture: objectives, teacher narration blocks, key terms, exam tips, board summary, quiz (MCQ with explanations), homework.
* Light/Dark theme, Naskh / Nastaliq Urdu fonts, text-size and "Class mode" (big text for projector), speech speed,
  progress tracking, search, "continue where I stopped", optional auto-play of the next lecture.

## Project layout

```
app/src/main/java/pk/ustad/lectures/   Kotlin shell: MainActivity (WebView + asset loader), TtsBridge (TextToSpeech)
app/src/main/assets/web/
  index.html  css/app.css
  js/core.js      registries (Chapters, Lectures, Diagrams) + inline markup
  js/kit.js       SVG helper kit (boxes, arrows, logic gates, grids, themed classes)
  js/speech.js    Urdish segmentation, TeX -> speech, TTS engine abstraction (Android bridge / browser fallback)
  js/app.js       home, lecture renderer, player, quiz, settings
  js/data/*.js        lecture content, one file per chapter part
  js/diagrams/*.js    SVG diagrams, one file per chapter part
  vendor/mathjax/tex-svg.js   MathJax 3 (offline)   fonts/  Noto Naskh Arabic, Noto Nastaliq Urdu
docs/CONTENT_SPEC.md   how lectures and diagrams are authored
tools/                 validator, diagram contact-sheet renderer, screenshot + player test harness
```

## Build the APK

```bash
export ANDROID_HOME=/path/to/android-sdk      # platforms;android-34, build-tools;34.0.0
./gradlew assembleDebug
# -> app/build/outputs/apk/debug/app-debug.apk
```

## Voices on the phone

Urdish needs two TTS voices. Install **Speech Services by Google** and download **Urdu (Pakistan)** and **English (India)**
voice data (Settings → System → Languages → Text-to-speech → Install voice data). The app shows a banner with shortcuts
if the Urdu voice is missing, and Settings → *Test Urdish voice* plays a sample sentence.

## Authoring and QA tools

```bash
cd tools && npm install                     # once (MathJax for TeX validation, puppeteer-core)
node tools/validate.js [key ...]            # structure, Urdu/English balance, diagram ids, real MathJax TeX check
node tools/sheet.js xi-1a /tmp/sheet.png    # contact sheet of every diagram in js/diagrams/xi-1a.js
NODE_PATH=tools/node_modules node tools/shot.js "#lec=xi-1-01" /tmp/l.png 390 800 scroll:0     # phone screenshot
NODE_PATH=tools/node_modules node tools/test-player.js xi-1-01       # player/TTS protocol test with a mock bridge
```

(`shot.js`, `sheet.js` and `test-player.js` use Chrome at `/opt/google/chrome/chrome`; edit the path if needed.)
