# CS XI Ultimate Coaching

Bilingual (English · Urdish · Urdu) teach-yourself coaching app for **Sindh Curriculum 2026, Class XI Computer Science, Units 1–6**.

The APK embeds every Learn + diagram page from the two Teach-Yourself booklets and speaks classroom coaching in **Urdish** (Roman Urdu with English technical terms, the same mix teachers use and the exam paper expects).

## Download

**Latest (v1.0.1)** — stacked embedded diagrams (no swipe) + Urdish TTS:

https://github.com/shahzadasahab/-1/raw/cursor/cs-xi-ultimate-coaching-74ef/releases/CsxiUltimateCoaching-v1.0.1-debug.apk

> Uninstall any older unrelated APK from this repo first. The package id is `com.csxi.ultimatecoaching`.

## What is inside

- **6 units, 40 lessons** mapped to the booklet contents (logic gates, SDLC, OSI/TCP-IP, algorithms, Python, Access, IoT/AI, digital inquiry).
- **Urdish Coach** on Home, every lesson, and every mock question. Uses the English TTS engine so it works when an Urdu voice pack is missing.
- **Embedded diagrams**: each exam figure and booklet page is stacked in the lesson (no swipe strip). Tap a page to zoom.
- **Check yourself**, **I can…** tracker, **unit mock tests**, searchable **glossary**.
- Languages: English UI, Urdish UI (default), اردو UI (RTL).

This is an independent study aid prepared from the Sindh Textbook Board Class XI Computer Science booklets. It is not an official publication.

## Build

```bash
python3 scripts/build_csxi_assets.py
export ANDROID_HOME=$HOME/android-sdk
./gradlew assembleDebug
```

Copy the APK from `app/build/outputs/apk/debug/` to `releases/`.
