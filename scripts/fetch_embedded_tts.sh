#!/usr/bin/env bash
# Download the embedded male Urdu teaching voice (Piper Fasih, ur_PK)
# and a slim sherpa-onnx Android AAR (arm64 + armeabi-v7a).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ASSETS="$ROOT/app/src/main/assets/tts/ur_male"
LIBS="$ROOT/app/libs"
WORK="${TMPDIR:-/tmp}/cs-tutor-tts"
MODEL_URL="https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-ur_PK-fasih-medium.tar.bz2"
AAR_URL="https://github.com/k2-fsa/sherpa-onnx/releases/download/v1.13.8/sherpa-onnx-1.13.8.aar"

mkdir -p "$ASSETS" "$LIBS" "$WORK"
if [[ ! -f "$ASSETS/ur_PK-fasih-medium.onnx" ]]; then
  echo "Downloading male Urdu voice (Fasih)…"
  curl -fL --retry 4 --retry-delay 3 -o "$WORK/ur.tbz2" "$MODEL_URL"
  tar -xjf "$WORK/ur.tbz2" -C "$WORK"
  SRC="$WORK/vits-piper-ur_PK-fasih-medium"
  cp "$SRC/ur_PK-fasih-medium.onnx" "$SRC/tokens.txt" "$ASSETS/"
  rm -rf "$ASSETS/espeak-ng-data"
  cp -a "$SRC/espeak-ng-data" "$ASSETS/espeak-ng-data"

  # Keep only Urdu + English espeak data (the teaching pair).
  KEEP="$ASSETS/espeak-ng-data"
  TMP="$WORK/espeak-slim"
  rm -rf "$TMP"
  mkdir -p "$TMP/lang/inc" "$TMP/lang/gmw"
  for f in phondata phonindex phontab intonations phondata-manifest ur_dict en_dict; do
    [[ -e "$KEEP/$f" ]] && cp -a "$KEEP/$f" "$TMP/"
  done
  [[ -d "$KEEP/voices" ]] && cp -a "$KEEP/voices" "$TMP/"
  [[ -e "$KEEP/lang/inc/ur" ]] && cp -a "$KEEP/lang/inc/ur" "$TMP/lang/inc/"
  [[ -e "$KEEP/lang/gmw/en" ]] && cp -a "$KEEP/lang/gmw/en" "$TMP/lang/gmw/"
  [[ -e "$KEEP/lang/gmw/en-US" ]] && cp -a "$KEEP/lang/gmw/en-US" "$TMP/lang/gmw/"
  rm -rf "$KEEP"
  mv "$TMP" "$KEEP"
  echo "Voice installed at $ASSETS"
fi

if [[ ! -f "$LIBS/sherpa-onnx-android-arm.aar" ]]; then
  echo "Downloading sherpa-onnx Android AAR…"
  curl -fL --retry 4 --retry-delay 3 -o "$WORK/sherpa.aar" "$AAR_URL"
  mkdir -p "$WORK/aar"
  rm -rf "$WORK/aar"/*
  unzip -qo "$WORK/sherpa.aar" -d "$WORK/aar"
  rm -rf "$WORK/aar/jni/x86" "$WORK/aar/jni/x86_64" "$WORK/aar/jni/armeabi-v7a"
  (cd "$WORK/aar" && zip -qr "$LIBS/sherpa-onnx-android-arm.aar" .)
  echo "AAR installed at $LIBS/sherpa-onnx-android-arm.aar"
fi
echo "Embedded TTS assets ready."
