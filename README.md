# CS XI & XII Teach Yourself — 30-Day Crash Course

Preparatory material for the **New Sindh Curriculum 2026**, built from the bilingual Teacher’s Edition booklets (Class XI Units 1–6 and Class XII Units 1–6).

- On-screen pages are the **printed booklets**, so every symbol, logic gate, truth table, K-map, chart and diagram is inside the app.
- An **embedded male Urdu teacher** (Piper Fasih, ur-PK) explains each lesson. No extra TTS install is required for Urdu.
- Every booklet page has **embedded tutor text**: Urdu description, with English exam terms in `{braces}` so the voice says them as printed.
- Critical exam terms stay **English as printed**: `Algorithm`, `Logic Gates`, `SDLC`, `Neural Networks`, `MVP`.
- Booklet pages turn automatically with the tutor.
- Each day is a **3-hour block**: Recap · Teach · Drill · 5-mark homework.

## Download

Version **2.1.0** puts the tutor’s words in the app as text: Urdu description, English exam terms in `{braces}`. Rebuild the APK to install that version (`./gradlew assembleDebug`). The home screen should then read **Version 2.1.0 — Urdu descriptions and English terms embedded as tutor text**.

The APK already stored in this repo is the previous **2.0.0** build (diagrams, symbols, and the Urdu voice, without the per-page tutor text):

https://github.com/shahzadasahab/-1/raw/cursor/cs-30day-teach-yourself-2ef7/releases/CS-XI-XII-TeachYourself-v2.0.0-urdu-tts-debug.apk

Repo copy: `releases/CS-XI-XII-TeachYourself-v2.0.0-urdu-tts-debug.apk`

That file is arm64. Install it on a 64-bit Android phone. Uninstall any older crash-course build first.

## How to use

1. Open **Computer Science XI** or **XII**. Wait until the day screen shows **Voice: Embedded male tutor · Fasih (ur-PK)**.
2. Open a day. The lesson plan is on screen in English. The booklet pages for that day are the scans.
3. Tap **Listen as tutor**. The teacher speaks Urdu and the page turns with each cue. When he names a figure, copy the printed diagram.
4. `{English terms}` in the tutor text are pronounced as written — do not translate them. Tap **Tutor text** to read the script.
5. Pinch or double-tap a page to zoom the symbols. Use **Speed** for 0.8x / 1.0x / 1.25x.
6. Tick the session when the 3-hour block is done.

Days 1–23 teach, chapter-end days are checkpoints, 24–26 Golden blitz, 27 recap, 28 mock, 29 mark, 30 repair.

## Build

```bash
python3 scripts/build_preparatory_course.py   # pages.json, course.json, and tts.json
bash scripts/fetch_embedded_tts.sh            # male Fasih voice + sherpa-onnx AAR
export ANDROID_HOME=/path/to/android-sdk
./gradlew assembleDebug
```

The combined booklet is `app/src/main/assets/course/crash-course.pdf` (288 pages). Voice models are not stored in git; Gradle downloads them and packs them into the APK.

## Version 2.1.0

- Each of the 288 booklet pages has embedded tutor text in `tts.json`.
- The description is Urdu. Exam terminology stays inside `{braces}` and is spoken in English, as printed.
- **Tutor text** on the day screen shows that same script, with the braces removed so it can be read.
- Listen as tutor, and Tutor this scan, speak this embedded text. Page turns still follow the lecture.

## Version 2.0.0

- Teach Yourself preparatory edition from the four bilingual Teacher’s Edition booklets.
- All 288 printed pages are embedded, including symbols and diagrams. Every page belongs to a day.
- Urdu tutoring scripts for 30 XI days and 30 XII days. English exam terms stay in braces and are spoken as printed.
- Figure cues tell the student to look at the embedded diagram and redraw it.
- arm64-only so the embedded voice and the full booklet fit in one sideload APK.
- Not tested on a physical device in the build environment.
