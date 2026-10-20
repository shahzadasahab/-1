package com.cslectures.notes

import android.annotation.SuppressLint
import android.os.Bundle
import android.view.WindowManager
import android.webkit.JavascriptInterface
import android.net.Uri
import android.webkit.WebResourceRequest
import android.webkit.WebResourceResponse
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.appcompat.app.AppCompatActivity
import androidx.webkit.WebViewAssetLoader
import com.cslectures.notes.databinding.ActivityLectureReaderBinding

class LectureReaderActivity : AppCompatActivity(), EmbeddedSpeaker.Listener {
    private lateinit var binding: ActivityLectureReaderBinding
    private lateinit var lecture: Lecture
    private lateinit var speaker: EmbeddedSpeaker
    private var startIndex = 0
    private var speedIndex = 1
    private val speeds = floatArrayOf(0.9f, 1.0f, 1.15f)
    private val speedLabels = arrayOf("0.9×", "1.0×", "1.15×")

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val found = LectureRepository.find(this, intent.getStringExtra(EXTRA_ID).orEmpty())
        if (found == null) {
            finish()
            return
        }
        lecture = found
        speaker = (application as LectureApp).speaker
        binding = ActivityLectureReaderBinding.inflate(layoutInflater)
        setContentView(binding.root)
        binding.toolbar.title = lecture.title
        binding.toolbar.subtitle = lecture.kicker
        binding.toolbar.setNavigationOnClickListener {
            speaker.stop()
            finish()
        }

        val assetLoader = WebViewAssetLoader.Builder()
            .addPathHandler("/assets/", WebViewAssetLoader.AssetsPathHandler(this))
            .build()
        binding.page.settings.javaScriptEnabled = true
        binding.page.settings.domStorageEnabled = false
        binding.page.settings.allowFileAccess = false
        binding.page.settings.builtInZoomControls = false
        binding.page.settings.displayZoomControls = false
        binding.page.webViewClient = object : WebViewClient() {
            override fun shouldInterceptRequest(
                view: WebView,
                request: WebResourceRequest,
            ): WebResourceResponse? = assetLoader.shouldInterceptRequest(request.url)

            @Deprecated("Needed so the main document is also served from assets")
            override fun shouldInterceptRequest(view: WebView, url: String): WebResourceResponse? =
                assetLoader.shouldInterceptRequest(Uri.parse(url))
        }
        binding.page.addJavascriptInterface(Picker(), "LectureBridge")
        binding.page.loadUrl("$ASSET_ROOT/notes/index.html#${lecture.id}")

        binding.play.setOnClickListener {
            speaker.speak(lecture.blocks, startIndex, speeds[speedIndex])
        }
        binding.pause.setOnClickListener { speaker.pause() }
        binding.resume.setOnClickListener { speaker.resume() }
        binding.stop.setOnClickListener {
            speaker.stop()
            window.clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
        }
        binding.speed.setOnClickListener {
            speedIndex = (speedIndex + 1) % speeds.size
            binding.speed.text = getString(R.string.speed_label, speedLabels[speedIndex])
        }
        binding.speed.text = getString(R.string.speed_label, speedLabels[speedIndex])
        speaker.listener = this
    }

    override fun onResume() {
        super.onResume()
        speaker.listener = this
    }

    override fun onDestroy() {
        if (isFinishing) speaker.stop()
        super.onDestroy()
    }

    override fun onEngineReady(ready: Boolean, message: String) {
        binding.voiceStatus.text = if (ready) {
            getString(R.string.voice_ready)
        } else {
            getString(R.string.voice_failed, message)
        }
        binding.play.isEnabled = ready
    }

    override fun onPlayback(speaking: Boolean, paused: Boolean) {
        if (speaking) {
            window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
            binding.voiceStatus.text = if (paused) {
                getString(R.string.paused)
            } else {
                getString(R.string.speaking)
            }
        } else {
            window.clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
            binding.voiceStatus.text = getString(R.string.voice_ready)
        }
        binding.pause.isEnabled = speaking && !paused
        binding.resume.isEnabled = speaking && paused
    }

    override fun onBlock(index: Int) {
        val id = org.json.JSONObject.quote(lecture.id)
        binding.page.evaluateJavascript("highlightBlock($id, $index)", null)
    }

    private inner class Picker {
        @JavascriptInterface
        fun pick(index: Int) {
            runOnUiThread {
                startIndex = index
                binding.voiceStatus.text = getString(R.string.starts_here, index + 1)
            }
        }
    }

    companion object {
        const val EXTRA_ID = "lecture_id"
        private const val ASSET_ROOT = "https://appassets.androidplatform.net/assets"
    }
}
