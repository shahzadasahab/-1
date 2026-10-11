package com.sindhcs.crashcourse.util

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.speech.tts.TextToSpeech
import android.speech.tts.UtteranceProgressListener
import android.speech.tts.Voice
import java.util.Locale
import java.util.concurrent.Executors
import java.util.concurrent.Future
import java.util.concurrent.atomic.AtomicBoolean

/**
 * Male teaching voice: prefers the embedded Fasih (ur-PK) engine shipped in the APK.
 * Falls back to a system male voice. {English terms} stay as printed.
 */
class MixedVoiceNarrator(
    private val context: Context,
    private val onReadyChanged: (Boolean) -> Unit,
    private val onSpeakingChanged: (Boolean) -> Unit,
    private val onLanguageIssue: ((String) -> Unit)? = null,
    private val onScriptFinished: (() -> Unit)? = null,
    private val onVoiceReady: ((String) -> Unit)? = null
) : TextToSpeech.OnInitListener {

    data class Segment(val text: String, val englishTerm: Boolean, val pauseMs: Long = 0)

    private val main = Handler(Looper.getMainLooper())
    private val worker = Executors.newSingleThreadExecutor()
    private var tts: TextToSpeech? = null
    private var embedded: EmbeddedMaleVoice? = null
    private var isReady = false
    private var systemReady = false
    private var embedTried = false
    private var announced = false
    private var urduAvailable = false
    private var useEmbedded = false
    private val pending = mutableListOf<String>()
    private var queue = ArrayDeque<Pair<Segment, String>>()
    private var speaking = false
    private var rateScale = 1.0f
    private val cancel = AtomicBoolean(false)
    private var job: Future<*>? = null
    @Volatile var voiceLabel: String = "System TTS"
        private set

    init {
        worker.execute {
            val male = EmbeddedMaleVoice(context)
            if (male.load()) {
                embedded = male
                useEmbedded = true
                voiceLabel = male.label
                urduAvailable = true
            }
            embedTried = true
            main.post { finishInit() }
        }
        tts = TextToSpeech(context.applicationContext, this)
    }

    override fun onInit(status: Int) {
        systemReady = status == TextToSpeech.SUCCESS
        if (systemReady) {
            tts?.setSpeechRate(0.82f * rateScale)
            tts?.setPitch(MALE_PITCH)
            attachProgressListener()
        }
        finishInit()
    }

    private fun finishInit() {
        if (!embedTried) return
        if (announced) return
        if (useEmbedded) {
            announced = true
            isReady = true
            onVoiceReady?.invoke(voiceLabel)
            onReadyChanged(true)
            flushPending()
            return
        }
        if (systemReady) {
            announced = true
            urduAvailable = localeAvailable(URDU_LOCALES)
            isReady = true
            voiceLabel = if (urduAvailable) {
                "System male tutor (Urdu)"
            } else {
                "System TTS · install Urdu for full lectures"
            }
            if (!urduAvailable) {
                onLanguageIssue?.invoke(
                    "Embedded male voice could not load. Install Urdu TTS, or rebuild with scripts/fetch_embedded_tts.sh."
                )
            }
            onVoiceReady?.invoke(voiceLabel)
            onReadyChanged(true)
            flushPending()
        } else {
            onReadyChanged(false)
        }
    }

    fun speakScript(script: String): Boolean {
        if (script.isBlank()) return false
        if (!isReady) {
            pending.add(script)
            return true
        }
        cancel.set(true)
        job?.cancel(true)
        embedded?.stop()
        tts?.stop()
        queue.clear()
        parseSegments(script).forEachIndexed { index, segment ->
            if (!segment.englishTerm && !urduAvailable && !useEmbedded) return@forEachIndexed
            chunk(segment.text).forEach { part ->
                queue.addLast(segment.copy(text = part) to "seg_${index}_${part.hashCode()}")
                val pause = when {
                    part.endsWith('۔') -> 420L
                    part.endsWith('.') || part.endsWith('?') -> 360L
                    segment.englishTerm -> 180L
                    else -> 220L
                }
                queue.addLast(Segment("", false, pause) to "pause_${index}_${part.hashCode()}")
            }
        }
        if (queue.isEmpty()) return false
        speaking = true
        onSpeakingChanged(true)
        cancel.set(false)
        if (useEmbedded && embedded?.ready == true) {
            val snapshot = ArrayList(queue)
            queue.clear()
            job = worker.submit { speakEmbedded(snapshot) }
        } else {
            speakNext(flush = true)
        }
        return true
    }

    fun setRateScale(scale: Float) {
        rateScale = scale.coerceIn(0.5f, 2.0f)
    }

    fun stop() {
        cancel.set(true)
        pending.clear()
        queue.clear()
        job?.cancel(true)
        embedded?.stop()
        tts?.stop()
        speaking = false
        onSpeakingChanged(false)
    }

    fun shutdown() {
        stop()
        embedded?.release()
        embedded = null
        tts?.shutdown()
        tts = null
        isReady = false
        worker.shutdownNow()
    }

    fun isSpeaking(): Boolean = speaking

    fun usesEmbeddedMale(): Boolean = useEmbedded

    private fun speakEmbedded(items: List<Pair<Segment, String>>) {
        val voice = embedded ?: return
        for ((segment, _) in items) {
            if (cancel.get()) break
            if (segment.pauseMs > 0) {
                try {
                    Thread.sleep(segment.pauseMs)
                } catch (_: InterruptedException) {
                    break
                }
                continue
            }
            val speed = (if (segment.englishTerm) 0.90f else 0.86f) * rateScale
            if (!voice.speakBlocking(segment.text, speed)) break
        }
        val finishedClean = !cancel.get()
        main.post {
            speaking = false
            onSpeakingChanged(false)
            if (finishedClean) onScriptFinished?.invoke()
        }
    }

    private fun flushPending() {
        if (pending.isEmpty()) return
        val queued = pending.toList()
        pending.clear()
        queued.forEach { speakScript(it) }
    }

    private fun speakNext(flush: Boolean) {
        val engine = tts ?: return
        val item = queue.removeFirstOrNull()
        if (item == null) {
            speaking = false
            onSpeakingChanged(false)
            onScriptFinished?.invoke()
            return
        }
        val (segment, id) = item
        val mode = if (flush) TextToSpeech.QUEUE_FLUSH else TextToSpeech.QUEUE_ADD
        if (segment.pauseMs > 0) {
            engine.playSilentUtterance(segment.pauseMs, mode, id)
            return
        }
        applyLocale(engine, segment.englishTerm)
        val params = Bundle().apply {
            putString(TextToSpeech.Engine.KEY_PARAM_UTTERANCE_ID, id)
        }
        engine.speak(segment.text, mode, params, id)
    }

    private fun attachProgressListener() {
        tts?.setOnUtteranceProgressListener(object : UtteranceProgressListener() {
            override fun onStart(utteranceId: String?) {
                speaking = true
                onSpeakingChanged(true)
            }

            override fun onDone(utteranceId: String?) {
                if (useEmbedded) return
                speakNext(flush = false)
            }

            @Deprecated("Deprecated in Java")
            override fun onError(utteranceId: String?) {
                if (useEmbedded) return
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
                selectMaleVoice(engine, locale)
                engine.setPitch(MALE_PITCH)
                engine.setSpeechRate((if (englishTerm) 0.76f else 0.82f) * rateScale)
                return
            }
        }
    }

    private fun localeAvailable(locales: List<Locale>): Boolean {
        val engine = tts ?: return false
        return locales.any { engine.isLanguageAvailable(it) >= TextToSpeech.LANG_AVAILABLE }
    }

    private fun selectMaleVoice(engine: TextToSpeech, locale: Locale) {
        val voices = engine.voices ?: return
        val match = voices
            .filter { it.locale.language == locale.language && !it.isNetworkConnectionRequired }
            .maxByOrNull { maleVoiceScore(it) }
        if (match != null) engine.voice = match
    }

    private fun maleVoiceScore(voice: Voice): Int {
        val name = voice.name.lowercase()
        var score = 0
        if (FEMALE_HINT.any { name.contains(it) }) score -= 8
        if (MALE_HINT.any { name.contains(it) }) score += 8
        if (voice.quality >= Voice.QUALITY_HIGH) score += 2
        if (!name.contains("network")) score += 1
        return score
    }

    companion object {
        private val URDU_LOCALES = listOf(Locale("ur", "PK"), Locale("ur", "IN"), Locale("ur"))
        private val ENGLISH_LOCALES = listOf(Locale.US, Locale.UK, Locale.ENGLISH)
        private val TERM = Regex("\\{([^{}]+)\\}")
        private const val MAX_CHUNK = 1800
        private const val MALE_PITCH = 0.88f
        private val MALE_HINT = listOf("male", "man", "fasih", "ravi", "david", "daniel", "mark", "ryan", "guy")
        private val FEMALE_HINT = listOf("female", "woman", "zira", "samantha", "salli", "ivy", "joanna", "kendra")

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
