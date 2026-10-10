package com.sindhcs.crashcourse.util

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.speech.tts.TextToSpeech
import android.speech.tts.UtteranceProgressListener
import android.speech.tts.Voice
import java.util.Locale

/**
 * Speaks Urdu lecture prose and switches to an English voice for {term} markers
 * so exam terminology is pronounced as printed on the booklet pages.
 */
class MixedVoiceNarrator(
    private val context: Context,
    private val onReadyChanged: (Boolean) -> Unit,
    private val onSpeakingChanged: (Boolean) -> Unit,
    private val onLanguageIssue: ((String) -> Unit)? = null
) : TextToSpeech.OnInitListener {

    data class Segment(val text: String, val englishTerm: Boolean)

    private var tts: TextToSpeech? = null
    private var isReady = false
    private var urduAvailable = false
    private val pending = mutableListOf<String>()
    private var queue = ArrayDeque<Pair<Segment, String>>()
    private var speaking = false
    private var rateScale = 1.0f

    init {
        tts = TextToSpeech(context.applicationContext, this)
    }

    override fun onInit(status: Int) {
        isReady = status == TextToSpeech.SUCCESS
        if (isReady) {
            tts?.setSpeechRate(0.88f * rateScale)
            tts?.setPitch(1.0f)
            urduAvailable = localeAvailable(URDU_LOCALES)
            attachProgressListener()
            if (!urduAvailable) {
                onLanguageIssue?.invoke(
                    "Urdu voice is not installed, so only the English text will be read. Install Urdu TTS for full lectures."
                )
            }
        }
        onReadyChanged(isReady)
        if (isReady && pending.isNotEmpty()) {
            val queued = pending.toList()
            pending.clear()
            queued.forEach { speakScript(it) }
        }
    }

    fun speakScript(script: String): Boolean {
        if (script.isBlank()) return false
        val engine = tts ?: return false
        if (!isReady) {
            pending.add(script)
            return true
        }
        engine.stop()
        queue.clear()
        parseSegments(script).forEachIndexed { index, segment ->
            if (!segment.englishTerm && !urduAvailable) return@forEachIndexed
            chunk(segment.text).forEach { part ->
                queue.addLast(segment.copy(text = part) to "seg_${index}_${part.hashCode()}")
            }
        }
        if (queue.isEmpty()) return false
        speaking = true
        onSpeakingChanged(true)
        speakNext(flush = true)
        return true
    }

    fun setRateScale(scale: Float) {
        rateScale = scale.coerceIn(0.5f, 2.0f)
    }

    fun stop() {
        pending.clear()
        queue.clear()
        tts?.stop()
        speaking = false
        onSpeakingChanged(false)
    }

    fun shutdown() {
        stop()
        tts?.shutdown()
        tts = null
        isReady = false
    }

    fun isSpeaking(): Boolean = speaking

    private fun speakNext(flush: Boolean) {
        val engine = tts ?: return
        val item = queue.removeFirstOrNull()
        if (item == null) {
            speaking = false
            onSpeakingChanged(false)
            return
        }
        val (segment, id) = item
        applyLocale(engine, segment.englishTerm)
        val params = Bundle().apply {
            putString(TextToSpeech.Engine.KEY_PARAM_UTTERANCE_ID, id)
        }
        val mode = if (flush) TextToSpeech.QUEUE_FLUSH else TextToSpeech.QUEUE_ADD
        engine.speak(segment.text, mode, params, id)
    }

    private fun attachProgressListener() {
        tts?.setOnUtteranceProgressListener(object : UtteranceProgressListener() {
            override fun onStart(utteranceId: String?) {
                speaking = true
                onSpeakingChanged(true)
            }

            override fun onDone(utteranceId: String?) {
                speakNext(flush = false)
            }

            @Deprecated("Deprecated in Java")
            override fun onError(utteranceId: String?) {
                speaking = false
                queue.clear()
                onSpeakingChanged(false)
            }

            override fun onError(utteranceId: String?, errorCode: Int) {
                onError(utteranceId)
            }
        })
    }

    private fun applyLocale(engine: TextToSpeech, englishTerm: Boolean) {
        val locales = if (englishTerm || !urduAvailable) ENGLISH_LOCALES else URDU_LOCALES
        for (locale in locales) {
            if (engine.isLanguageAvailable(locale) >= TextToSpeech.LANG_AVAILABLE) {
                engine.language = locale
                selectBestVoice(engine, locale)
                engine.setSpeechRate((if (englishTerm) 0.82f else 0.88f) * rateScale)
                return
            }
        }
    }

    private fun localeAvailable(locales: List<Locale>): Boolean {
        val engine = tts ?: return false
        return locales.any { engine.isLanguageAvailable(it) >= TextToSpeech.LANG_AVAILABLE }
    }

    private fun selectBestVoice(engine: TextToSpeech, locale: Locale) {
        val voices = engine.voices ?: return
        val match = voices
            .filter { it.locale.language == locale.language && !it.isNetworkConnectionRequired }
            .maxByOrNull { voiceScore(it) }
        if (match != null) engine.voice = match
    }

    private fun voiceScore(voice: Voice): Int {
        var score = 0
        if (voice.quality >= Voice.QUALITY_HIGH) score += 2
        if (!voice.name.contains("network", ignoreCase = true)) score += 1
        return score
    }

    companion object {
        private val URDU_LOCALES = listOf(Locale("ur", "PK"), Locale("ur", "IN"), Locale("ur"))
        private val ENGLISH_LOCALES = listOf(Locale.US, Locale.UK, Locale.ENGLISH)
        private val TERM = Regex("\\{([^{}]+)\\}")
        private const val MAX_CHUNK = 1800

        fun parseSegments(script: String): List<Segment> {
            val out = mutableListOf<Segment>()
            var last = 0
            for (match in TERM.findAll(script)) {
                if (match.range.first > last) {
                    val urdu = script.substring(last, match.range.first).trim()
                    if (urdu.isNotEmpty()) out.add(Segment(urdu, false))
                }
                val term = match.groupValues[1].trim()
                if (term.isNotEmpty()) out.add(Segment(term, true))
                last = match.range.last + 1
            }
            if (last < script.length) {
                val tail = script.substring(last).trim()
                if (tail.isNotEmpty()) out.add(Segment(tail, false))
            }
            return out.filter { it.text.isNotBlank() }
        }

        fun visibleTranscript(script: String): String =
            script.replace("{", "").replace("}", "")

        private fun chunk(text: String): List<String> {
            if (text.length <= MAX_CHUNK) return listOf(text)
            val chunks = mutableListOf<String>()
            var remaining = text.trim()
            while (remaining.isNotEmpty()) {
                if (remaining.length <= MAX_CHUNK) {
                    chunks.add(remaining)
                    break
                }
                var splitAt = remaining.lastIndexOf('۔', MAX_CHUNK)
                if (splitAt < MAX_CHUNK / 2) splitAt = remaining.lastIndexOf('.', MAX_CHUNK)
                if (splitAt < MAX_CHUNK / 2) splitAt = remaining.lastIndexOf(' ', MAX_CHUNK)
                if (splitAt <= 0) splitAt = MAX_CHUNK
                chunks.add(remaining.substring(0, splitAt + 1).trim())
                remaining = remaining.substring(splitAt + 1).trim()
            }
            return chunks.ifEmpty { listOf(text) }
        }

        fun openTtsSettings(context: Context) {
            val intents = listOf(
                Intent(TextToSpeech.Engine.ACTION_INSTALL_TTS_DATA),
                Intent("com.android.settings.TTS_SETTINGS"),
                Intent(android.provider.Settings.ACTION_SETTINGS)
            )
            for (intent in intents) {
                if (intent.resolveActivity(context.packageManager) != null) {
                    intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                    context.startActivity(intent)
                    return
                }
            }
        }
    }
}
