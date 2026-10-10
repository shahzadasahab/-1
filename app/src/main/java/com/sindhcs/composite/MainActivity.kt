package com.sindhcs.composite

import android.annotation.SuppressLint
import android.content.Intent
import android.os.Bundle
import androidx.activity.OnBackPressedCallback
import android.webkit.JavascriptInterface
import android.webkit.WebChromeClient
import android.webkit.WebResourceRequest
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.sindhcs.composite.tts.VoiceNarrator

class MainActivity : AppCompatActivity() {

    private lateinit var webView: WebView
    private var narrator: VoiceNarrator? = null
    private var voiceReady = false

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        webView = WebView(this)
        setContentView(webView)

        narrator = VoiceNarrator(
            context = this,
            onReadyChanged = { ready -> voiceReady = ready },
            onSpeakingChanged = { speaking ->
                runOnUiThread {
                    webView.evaluateJavascript(
                        "window.CSCompositeNative && CSCompositeNative.onSpeaking(${speaking});",
                        null
                    )
                }
            },
            onLanguageIssue = { message ->
                runOnUiThread {
                    Toast.makeText(this, message, Toast.LENGTH_LONG).show()
                    val safe = message.replace("'", "\\'").replace("\n", " ")
                    webView.evaluateJavascript(
                        "window.CSCompositeNative && CSCompositeNative.onVoiceMessage('$safe');",
                        null
                    )
                }
            }
        )

        val settings = webView.settings
        settings.javaScriptEnabled = true
        settings.domStorageEnabled = true
        settings.allowFileAccess = true
        settings.allowContentAccess = true
        settings.useWideViewPort = true
        settings.loadWithOverviewMode = true
        settings.builtInZoomControls = true
        settings.displayZoomControls = false
        settings.mixedContentMode = android.webkit.WebSettings.MIXED_CONTENT_ALWAYS_ALLOW

        webView.webChromeClient = WebChromeClient()
        webView.webViewClient = object : WebViewClient() {
            override fun shouldOverrideUrlLoading(
                view: WebView?,
                request: WebResourceRequest?
            ): Boolean = false
        }
        webView.addJavascriptInterface(LectureBridge(), "AndroidLecture")
        webView.loadUrl("file:///android_asset/www/index.html")

        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                if (webView.canGoBack()) {
                    webView.goBack()
                } else {
                    isEnabled = false
                    onBackPressedDispatcher.onBackPressed()
                }
            }
        })
    }

    override fun onDestroy() {
        narrator?.shutdown()
        narrator = null
        webView.destroy()
        super.onDestroy()
    }

    inner class LectureBridge {
        @JavascriptInterface
        fun speakUrdu(text: String) {
            runOnUiThread {
                if (!voiceReady) {
                    Toast.makeText(this@MainActivity, R.string.voice_not_ready, Toast.LENGTH_SHORT).show()
                    return@runOnUiThread
                }
                if (narrator?.speakUrdu(text) != true) {
                    Toast.makeText(this@MainActivity, R.string.voice_install_prompt, Toast.LENGTH_LONG).show()
                    VoiceNarrator.openTtsSettings(this@MainActivity)
                }
            }
        }

        @JavascriptInterface
        fun stop() {
            runOnUiThread { narrator?.stop() }
        }

        @JavascriptInterface
        fun openPdf(fileName: String, page: Int) {
            runOnUiThread {
                startActivity(
                    Intent(this@MainActivity, PdfViewerActivity::class.java).apply {
                        putExtra(PdfViewerActivity.EXTRA_PDF, fileName)
                        putExtra(PdfViewerActivity.EXTRA_PAGE, page)
                    }
                )
            }
        }
    }
}
