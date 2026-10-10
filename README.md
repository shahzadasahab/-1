# CS XI & XII 30-Day Crash Course

Android reader for the **Computer Science XI and XII 30-Day Crash Course** (New Sindh Curriculum 2026).

- On-screen text is **English only**.
- Every booklet page is **embedded as printed** (204-page PDF).
- Each day has a **Urdu lecture** you can listen to.
- Exam terms stay **English as-is** on the page and in speech: `Algorithm`, `Logic Gates`, `SDLC`, `Neural Networks`, `MVP`.

## Download

**Latest (v1.1.0)** — page-faithful narration · zoom · speed control:

https://github.com/shahzadasahab/-1/raw/cursor/cs-crash-course-urdu-tts-66df/releases/CS-XI-XII-CrashCourse-v1.1.0-page-faithful-debug.apk

Repo copy: `releases/CS-XI-XII-CrashCourse-v1.1.0-page-faithful-debug.apk`

Uninstall any older version first. On the home screen you should see **Version 1.1.0 — English text · Urdu voice · page-faithful narration**.

## How to use

1. Install **Urdu** in Android Text-to-speech settings (Google TTS → install Urdu voice).
2. Open **Computer Science XI** or **XII**.
3. Open a day. Swipe the original booklet pages. On-screen notes stay English.
4. Tap **Listen lecture**. Spoken explanation is Urdu; `{English terms}` are pronounced as written.
5. Tap **This page** to hear the current booklet page: Urdu connecting phrases, with the printed English sentences read exactly as written. Open **Page text** to see that English text on screen.
6. Pinch or double-tap a page to zoom. Use **Speed** to switch between 0.8x, 1.0x and 1.25x.
7. Tick the day when the 3-hour block is done. The home screen offers **Continue** to jump back to the last day you opened.

Days 1–23 teach, chapter-end days are checkpoints, 24–26 Golden blitz, 27 recap, 28 mock, 29 mark, 30 repair.

## Build

```bash
python3 scripts/extract_pages.py      # pages.json from the PDF (needs pypdf)
python3 scripts/build_course_json.py  # course.json lectures
export ANDROID_HOME=/path/to/android-sdk
./gradlew assembleDebug
```

The debug APK is written to `app/build/outputs/apk/debug/`.

## Version 1.1.0

- "This page" narration is built from each page's printed text (`pages.json`): Urdu framing, English sentences spoken as-is.
- New "Page text" panel, pinch/double-tap zoom, async page rendering, speech speed control, keep-screen-on while speaking, Continue button on home.
- Lecture fixes: IDE, MS Access, and AI definitions now match the booklet; if Urdu TTS is missing only English text is read.
- Not tested on a physical device in the build environment.

## Version 1.0.1
