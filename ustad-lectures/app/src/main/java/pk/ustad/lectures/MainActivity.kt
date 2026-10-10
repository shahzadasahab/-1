package pk.ustad.lectures

import android.annotation.SuppressLint
import android.graphics.Color
import android.os.Bundle
import android.view.View
import android.view.ViewGroup
import android.webkit.ConsoleMessage
import android.webkit.JavascriptInterface
import android.webkit.WebChromeClient
import android.webkit.WebResourceRequest
import android.webkit.WebResourceResponse
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.OnBackPressedCallback
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.WindowCompat
import androidx.webkit.WebViewAssetLoader

class MainActivity : AppCompatActivity() {

    private lateinit var webView: WebView
    private lateinit var tts: TtsBridge

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        WindowCompat.setDecorFitsSystemWindows(window, true)

        webView = WebView(this).apply {
            layoutParams = ViewGroup.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.MATCH_PARENT,
            )
            setBackgroundColor(Color.parseColor("#F4F7F6"))
            overScrollMode = View.OVER_SCROLL_NEVER
        }
        setContentView(webView)

        val loader = WebViewAssetLoader.Builder()
            .setDomain(ASSET_HOST)
            .addPathHandler("/", WebViewAssetLoader.AssetsPathHandler(this))
            .build()

        webView.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true
            allowFileAccess = false
            allowContentAccess = false
            mediaPlaybackRequiresUserGesture = false
            cacheMode = WebSettings.LOAD_DEFAULT
            textZoom = 100
            setSupportZoom(false)
        }

        webView.webViewClient = object : WebViewClient() {
            override fun shouldInterceptRequest(
                view: WebView,
                request: WebResourceRequest,
            ): WebResourceResponse? = loader.shouldInterceptRequest(request.url)
        }
        webView.webChromeClient = object : WebChromeClient() {
            override fun onConsoleMessage(m: ConsoleMessage): Boolean {
                android.util.Log.d("UstadWeb", "${m.message()} (${m.sourceId()}:${m.lineNumber()})")
                return true
            }
        }

        tts = TtsBridge(this) { js -> webView.post { webView.evaluateJavascript(js, null) } }
        webView.addJavascriptInterface(tts, "AndroidTTS")
        webView.addJavascriptInterface(HostBridge(), "AndroidHost")

        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                webView.evaluateJavascript("(window.App && App.onBack && App.onBack()) ? '1' : '0'") { r ->
                    if (r == "\"1\"" || r == "1") return@evaluateJavascript
                    isEnabled = false
                    onBackPressedDispatcher.onBackPressed()
                }
            }
        })

        webView.loadUrl("https://$ASSET_HOST/web/index.html")
    }

    inner class HostBridge {
        @JavascriptInterface
        fun keepScreenOn(on: Boolean) {
            runOnUiThread {
                if (on) window.addFlags(android.view.WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
                else window.clearFlags(android.view.WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
            }
        }

        @JavascriptInterface
        fun setBars(color: String, dark: Boolean) {
            runOnUiThread {
                try {
                    val c = Color.parseColor(color)
                    window.statusBarColor = c
                    window.navigationBarColor = c
                    webView.setBackgroundColor(c)
                    val ctl = WindowCompat.getInsetsController(window, window.decorView)
                    ctl.isAppearanceLightStatusBars = !dark
                    ctl.isAppearanceLightNavigationBars = !dark
                } catch (_: Exception) {
                }
            }
        }
    }

    override fun onPause() {
        super.onPause()
        webView.evaluateJavascript("window.App && App.onHostPause && App.onHostPause()", null)
        tts.pause()
        webView.onPause()
    }

    override fun onResume() {
        super.onResume()
        webView.onResume()
        tts.refresh()
    }

    override fun onDestroy() {
        tts.shutdown()
        webView.removeJavascriptInterface("AndroidTTS")
        webView.destroy()
        super.onDestroy()
    }

    companion object {
        private const val ASSET_HOST = "appassets.androidplatform.net"
    }
}
