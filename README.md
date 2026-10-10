# CS XI & XII 30-Day Crash Course

Android reader for the **Computer Science XI and XII 30-Day Crash Course** (New Sindh Curriculum 2026).

- On-screen text is **English only**.
- Every booklet page is **embedded as printed** (204-page PDF).
- Each day has a **Urdu lecture** you can listen to.
- Exam terms stay **English as-is** on the page and in speech: `Algorithm`, `Logic Gates`, `SDLC`, `Neural Networks`, `MVP`.

## Download

**Latest (v1.0.1)** — English display · Urdu voice · terms as printed:

https://github.com/shahzadasahab/-1/raw/cursor/cs-crash-course-urdu-tts-66df/releases/CS-XI-XII-CrashCourse-v1.0.1-english-text-urdu-voice-debug.apk

Repo copy: `releases/CS-XI-XII-CrashCourse-v1.0.1-english-text-urdu-voice-debug.apk`

Uninstall any older version first. On the home screen you should see **Version 1.0.1 — English text · Urdu voice · terms as printed**.

## How to use

1. Install **Urdu** in Android Text-to-speech settings (Google TTS → install Urdu voice).
2. Open **Computer Science XI** or **XII**.
3. Open a day. Swipe the original booklet pages. On-screen notes stay English.
4. Tap **Listen lecture**. Spoken explanation is Urdu; `{English terms}` are pronounced as written.
5. Tick the day when the 3-hour block is done.

Days 1–23 teach, chapter-end days are checkpoints, 24–26 Golden blitz, 27 recap, 28 mock, 29 mark, 30 repair.

## Build

```bash
python3 scripts/build_course_json.py
export ANDROID_HOME=/path/to/android-sdk
./gradlew assembleDebug
```

The debug APK is written to `app/build/outputs/apk/debug/`.

## Version 1.0.1
