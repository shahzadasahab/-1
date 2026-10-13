# TTS bridge methods are called from the bundled WebView pages.
-keepclassmembers class com.sindhcs.cheatsheet.TtsBridge {
    @android.webkit.JavascriptInterface <methods>;
}
