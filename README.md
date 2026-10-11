# CS XI & XII Academic Tutor

Academic tutoring edition of the **Computer Science XI and XII 30-Day Crash Course** (New Sindh Curriculum 2026).

- On-screen text is **English only**.
- The tutor **speaks Urdu** and explains each session as a teacher would.
- Critical exam terms stay **English as printed**: `Algorithm`, `Logic Gates`, `SDLC`, `Neural Networks`, `MVP`.
- Every booklet page is **embedded as printed** (204-page PDF).
- Each day is a **3-hour tutoring block**: Recap · Teach · Drill · 5-mark homework.

## Download

**Latest (v1.2.0)** — academic tutoring edition · Urdu tutor · English terms as printed:

https://github.com/shahzadasahab/-1/raw/cursor/cs-crash-course-urdu-tts-66df/releases/CS-XI-XII-CrashCourse-v1.2.0-tutoring-edition-debug.apk

Repo copy: `releases/CS-XI-XII-CrashCourse-v1.2.0-tutoring-edition-debug.apk`

Uninstall any older version first. The home screen should read **Version 1.2.0 — Academic tutoring · English text · Urdu voice · terms as printed**.

## How to use

1. Install **Urdu** in Android Text-to-speech settings (Google TTS → install Urdu voice).
2. Open **Computer Science XI** or **XII**.
3. Open a day. The lesson plan is on screen in English. Swipe the original booklet pages.
4. Tap **Listen as tutor** for the full session, or pick a phase: Recap, Teach, Drill, 5-mark.
5. Spoken explanation is Urdu. `{English terms}` are pronounced as written — do not translate them.
6. Tap **Tutor this page** to walk the current booklet page: Urdu teaching, printed English sentences as-is.
7. Pinch or double-tap a page to zoom. Use **Speed** for 0.8x / 1.0x / 1.25x.
8. Tick the session when the 3-hour block is done. Home offers **Continue session**.

Days 1–23 teach, chapter-end days are checkpoints, 24–26 Golden blitz, 27 recap, 28 mock, 29 mark, 30 repair.

## Build

```bash
python3 scripts/extract_pages.py      # pages.json from the PDF (needs pypdf)
python3 scripts/build_course_json.py  # course.json lectures
export ANDROID_HOME=/path/to/android-sdk
./gradlew assembleDebug
```

The debug APK is written to `app/build/outputs/apk/debug/`.

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
