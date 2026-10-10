# CS XI–XII Composite

All-in-one offline Android reader for the Sindh / BIEK Computer Science teacher notes:

- Class XI bilingual lectures
- Class XII bilingual lectures
- Class XI Q&A masterpiece
- Class XII Q&A masterpiece

English text stays on screen. Device TTS speaks classroom-style **Urdu lectures**. Formulas render with **embedded MathJax SVG**. The shell is **Flexbox**. The four source PDFs are bundled and can be opened page-by-page.

## Download

After the debug APK is built it lives in `releases/CSComposite-v1.0.0-debug.apk`.

## Features

- English lecture notes and exam Q&A, cleaned from the four source PDFs
- Urdu explaining-lecture scripts for every topic
- Embedded MathJax 3 `tex-svg` (no network)
- Flexbox home, chapter, and topic layout
- Original PDF page viewer via Android `PdfRenderer`
- Works offline; Urdu voice uses the system TTS engine (`ur-PK` when installed)

## Build

```bash
python3 scripts/generate_catalog.py
export ANDROID_HOME=/home/ubuntu/android-sdk
./gradlew assembleDebug
```

Regenerate `app/src/main/assets/www/js/catalog.js` whenever the source PDFs change.

## Version 1.0.0
