# CS XI & XII Academic Tutor

Academic tutoring edition of the **Computer Science XI and XII 30-Day Crash Course** (New Sindh Curriculum 2026).

- On-screen text is **English only**.
- An **embedded male Urdu teacher** (Piper Fasih, ur-PK) explains each lecture. No extra TTS install is required for Urdu.
- Critical exam terms stay **English as printed**: `Algorithm`, `Logic Gates`, `SDLC`, `Neural Networks`, `MVP`.
- Booklet **scans turn automatically** with the tutor (page-synced autoplay).
- Every booklet page is **embedded as printed** (204-page PDF).
- Each day is a **3-hour tutoring block**: Recap · Teach · Drill · 5-mark homework.

## Download

**Latest (v1.3.0)** — embedded male tutor · page-synced scans:

https://github.com/shahzadasahab/-1/raw/cursor/cs-crash-course-urdu-tts-66df/releases/CS-XI-XII-CrashCourse-v1.3.0-male-tutor-synced-debug.apk

Repo copy: `releases/CS-XI-XII-CrashCourse-v1.3.0-male-tutor-synced-debug.apk`

Uninstall any older version first. The home screen should read **Version 1.3.0 — Male tutor · page-synced scans · English terms as printed**. The APK is larger because the male Urdu voice is inside it.

## How to use

1. Open **Computer Science XI** or **XII**. Wait until the day screen shows **Voice: Embedded male tutor · Fasih (ur-PK)**.
2. Open a day. The lesson plan is on screen in English.
3. Tap **Listen as tutor**. The male teacher speaks Urdu and the booklet scan turns with each cue.
4. Or pick a phase (Recap, Teach, Drill, 5-mark). **Teach** walks every scan in order.
5. `{English terms}` are pronounced as written — do not translate them.
6. Tap **Tutor this scan** to teach only the page on screen.
7. Pinch or double-tap a page to zoom. Use **Speed** for 0.8x / 1.0x / 1.25x.
8. Tick the session when the 3-hour block is done. Home offers **Continue session**.

Days 1–23 teach, chapter-end days are checkpoints, 24–26 Golden blitz, 27 recap, 28 mock, 29 mark, 30 repair.

## Build

```bash
python3 scripts/extract_pages.py      # pages.json from the PDF (needs pypdf)
python3 scripts/build_course_json.py  # course.json lectures
bash scripts/fetch_embedded_tts.sh    # male Fasih voice + sherpa-onnx AAR
export ANDROID_HOME=/path/to/android-sdk
./gradlew assembleDebug
```

The debug APK is written to `app/build/outputs/apk/debug/`. Gradle runs the fetch script if the voice files are missing. Voice models are not stored in git; they are packed into the APK.

## Version 1.3.0

- Embeds a male Urdu teaching voice (Piper Fasih, ur-PK) via sherpa-onnx. Built for intermediate / HSSC students.
- **Listen as tutor** auto-flips booklet scans in sync with the lecture (opening → each page → close).
- Teach phase is page-faithful: one cue per printed scan.
- Falls back to a system male voice if the embedded engine cannot load.
- Not tested on a physical device in the build environment.

## Version 1.2.0

- Academic tutoring edition: the voice is a teacher, not a page reader.
- Full session = opening + recap + teach + closed-book drill + tonight’s 5-mark close.
- Phase chips let you hear one part of the 3-hour block.
- “Tutor this page” uses printed page text with academic Urdu framing; English sentences stay as written.
- Lesson notes, exam-term rule, and 5-mark method (Define · Explain · Example · Diagram · Working) are on screen in English.
- Deliberate tutoring pace with short pauses between Urdu and English terms.
- Not tested on a physical device in the build environment.

## Version 1.1.0

- "This page" narration is built from each page's printed text (`pages.json`): Urdu framing, English sentences spoken as-is.
- New "Page text" panel, pinch/double-tap zoom, async page rendering, speech speed control, keep-screen-on while speaking, Continue button on home.
- Lecture fixes: IDE, MS Access, and AI definitions now match the booklet; if Urdu TTS is missing only English text is read.
- Not tested on a physical device in the build environment.

## Version 1.0.1
