package com.sindhcs.cheatsheet

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.speech.tts.TextToSpeech
import android.speech.tts.UtteranceProgressListener
import android.webkit.JavascriptInterface
import android.webkit.WebView
import org.json.JSONArray
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
    private var pendingCues: String? = null
    private var active = 0
    private var epoch = 0

    override fun onInit(status: Int) {
        ready = status == TextToSpeech.SUCCESS
        if (ready) {
            applySpokenLocale(engine!!)
            engine?.setSpeechRate(rate)
            engine?.setPitch(0.98f)
            engine?.setOnUtteranceProgressListener(object : UtteranceProgressListener() {
                override fun onStart(utteranceId: String?) {
                    if (!current(utteranceId)) return
                    notifyWeb(true)
                    val raw = callbackId(utteranceId)
                    if (!raw.startsWith(PREFIX)) notifyCue(raw)
                }

                override fun onDone(utteranceId: String?) {
                    if (!current(utteranceId)) return
                    active = (active - 1).coerceAtLeast(0)
                    if (active == 0) notifyWeb(false)
                }

                @Deprecated("Deprecated in Java")
                override fun onError(utteranceId: String?) {
                    if (!current(utteranceId)) return
                    active = 0
                    notifyWeb(false)
                }

                override fun onError(utteranceId: String?, errorCode: Int) {
                    if (!current(utteranceId)) return
                    active = 0
                    notifyWeb(false)
                }
            })
            val queuedCues = pendingCues
            val queuedText = pending
            pendingCues = null
            pending = null
            if (queuedCues != null) speakCues(queuedCues, rate.toDouble())
            else if (queuedText != null) speak(queuedText, rate.toDouble())
        }
    }

    @JavascriptInterface
    fun speak(text: String, speechRate: Double) {
        if (text.isBlank()) return
        rate = speechRate.toFloat().coerceIn(0.6f, 1.3f)
        val speaker = engine
        if (!ready || speaker == null) {
            pending = text
            pendingCues = null
            return
        }
        speaker.setSpeechRate(rate)
        val chunks = chunk(text)
        val generation = beginUtterances()
        active = chunks.size
        chunks.forEachIndexed { index, chunk ->
            val id = "$generation:" + PREFIX + index
            val params = Bundle().apply {
                putString(TextToSpeech.Engine.KEY_PARAM_UTTERANCE_ID, id)
            }
            val mode = if (index == 0) TextToSpeech.QUEUE_FLUSH else TextToSpeech.QUEUE_ADD
            speaker.speak(chunk, mode, params, id)
        }
    }

    @JavascriptInterface
    fun speakCues(json: String, speechRate: Double) {
        if (json.isBlank()) return
        rate = speechRate.toFloat().coerceIn(0.6f, 1.3f)
        val speaker = engine
        if (!ready || speaker == null) {
            pendingCues = json
            pending = null
            return
        }
        val items = ArrayList<Pair<String, String>>()
        try {
            val array = JSONArray(json)
            for (index in 0 until array.length()) {
                val obj = array.optJSONObject(index) ?: continue
                val text = obj.optString("t").trim()
                if (text.isEmpty()) continue
                val id = obj.optString("id").ifBlank { "cue_$index" }
                items.add(id to text)
            }
        } catch (_: Exception) {
            return
        }
        if (items.isEmpty()) return
        speaker.setSpeechRate(rate)
        val generation = beginUtterances()
        active = items.size
        items.forEachIndexed { index, (id, text) ->
            val tagged = "$generation:$id"
            val params = Bundle().apply {
                putString(TextToSpeech.Engine.KEY_PARAM_UTTERANCE_ID, tagged)
            }
            val mode = if (index == 0) TextToSpeech.QUEUE_FLUSH else TextToSpeech.QUEUE_ADD
            speaker.speak(text, mode, params, tagged)
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
        pendingCues = null
        active = 0
        epoch += 1
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
        pendingCues = null
        active = 0
        engine?.stop()
        engine?.shutdown()
        engine = null
        ready = false
    }

    private fun applySpokenLocale(speaker: TextToSpeech) {
        val candidates = listOf(Locale("en", "IN"), Locale.UK, Locale.US, Locale.ENGLISH)
        for (locale in candidates) {
            val available = speaker.isLanguageAvailable(locale)
            if (
                available == TextToSpeech.LANG_AVAILABLE ||
                available == TextToSpeech.LANG_COUNTRY_AVAILABLE ||
                available == TextToSpeech.LANG_COUNTRY_VAR_AVAILABLE
            ) {
                speaker.language = locale
                return
            }
        }
    }

    private fun beginUtterances(): Int {
        epoch += 1
        return epoch
    }

    private fun current(utteranceId: String?): Boolean {
        val mark = utteranceId?.substringBefore(':', "") ?: return false
        return mark == epoch.toString()
    }

    private fun callbackId(utteranceId: String?): String {
        return utteranceId?.substringAfter(':', "") ?: ""
    }

    private fun notifyCue(id: String) {
        val safe = id.replace("\\", "").replace("'", "")
        webView.post {
            webView.evaluateJavascript(
                "window.__ttsCue && window.__ttsCue('$safe')",
                null
            )
        }
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
