package com.sindhcs.cheatsheet

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.speech.tts.TextToSpeech
import android.speech.tts.UtteranceProgressListener
import android.webkit.JavascriptInterface
import android.webkit.WebView
import java.util.Locale

class TtsBridge(
    context: Context,
    private val webView: WebView
) : TextToSpeech.OnInitListener {

    private val appContext = context.applicationContext
    private var engine: TextToSpeech? = TextToSpeech(appContext, this)
    private var ready = false
    private var rate = 0.92f
    private var pending: String? = null
    private var active = 0

    override fun onInit(status: Int) {
        ready = status == TextToSpeech.SUCCESS
        if (ready) {
            engine?.language = Locale.US
            engine?.setSpeechRate(rate)
            engine?.setOnUtteranceProgressListener(object : UtteranceProgressListener() {
                override fun onStart(utteranceId: String?) {
                    notifyWeb(true)
                }

                override fun onDone(utteranceId: String?) {
                    if (utteranceId?.startsWith(PREFIX) == true) {
                        active = (active - 1).coerceAtLeast(0)
                    }
                    if (active == 0) notifyWeb(false)
                }

                @Deprecated("Deprecated in Java")
                override fun onError(utteranceId: String?) {
                    active = 0
                    notifyWeb(false)
                }

                override fun onError(utteranceId: String?, errorCode: Int) {
                    active = 0
                    notifyWeb(false)
                }
            })
            pending?.let { text ->
                pending = null
                speak(text, rate.toDouble())
            }
        }
    }

    @JavascriptInterface
    fun speak(text: String, speechRate: Double) {
        if (text.isBlank()) return
        rate = speechRate.toFloat().coerceIn(0.6f, 1.3f)
        val speaker = engine
        if (!ready || speaker == null) {
            pending = text
            return
        }
        speaker.setSpeechRate(rate)
        val chunks = chunk(text)
        active = chunks.size
        chunks.forEachIndexed { index, chunk ->
            val id = PREFIX + index
            val params = Bundle().apply {
                putString(TextToSpeech.Engine.KEY_PARAM_UTTERANCE_ID, id)
            }
            val mode = if (index == 0) TextToSpeech.QUEUE_FLUSH else TextToSpeech.QUEUE_ADD
            speaker.speak(chunk, mode, params, id)
        }
    }

    @JavascriptInterface
    fun setRate(speechRate: Double) {
        rate = speechRate.toFloat().coerceIn(0.6f, 1.3f)
        engine?.setSpeechRate(rate)
    }

    @JavascriptInterface
    fun stop() {
        pending = null
        active = 0
        engine?.stop()
        notifyWeb(false)
    }

    @JavascriptInterface
    fun openSettings() {
        val intents = listOf(
            Intent("com.android.settings.TTS_SETTINGS"),
            Intent(android.provider.Settings.ACTION_SETTINGS)
        )
        for (intent in intents) {
            if (intent.resolveActivity(appContext.packageManager) != null) {
                intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                appContext.startActivity(intent)
                return
            }
        }
    }

    fun shutdown() {
        pending = null
        active = 0
        engine?.stop()
        engine?.shutdown()
        engine = null
        ready = false
    }

    private fun notifyWeb(isSpeaking: Boolean) {
        webView.post {
            webView.evaluateJavascript(
                "window.__ttsState && window.__ttsState(${if (isSpeaking) "true" else "false"})",
                null
            )
        }
    }

    private fun chunk(text: String): List<String> {
        if (text.length <= MAX) return listOf(text)
        val chunks = mutableListOf<String>()
        var rest = text.trim()
        while (rest.isNotEmpty()) {
            if (rest.length <= MAX) {
                chunks.add(rest)
                break
            }
            var splitAt = rest.lastIndexOf('.', MAX)
            if (splitAt < MAX / 2) splitAt = rest.lastIndexOf(' ', MAX)
            if (splitAt <= 0) splitAt = MAX
            chunks.add(rest.substring(0, splitAt + 1).trim())
            rest = rest.substring(splitAt + 1).trim()
        }
        return chunks.ifEmpty { listOf(text) }
    }

    companion object {
        private const val MAX = 3200
        private const val PREFIX = "cs_"
    }
}
