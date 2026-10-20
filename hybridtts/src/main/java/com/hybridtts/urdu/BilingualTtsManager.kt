package com.hybridtts.urdu

import android.content.Context
import android.speech.tts.TextToSpeech
import android.speech.tts.UtteranceProgressListener
import java.util.Locale

enum class TtsMode {
    /** One ur-PK voice reads Urdu script and the embedded English words. */
    SMOOTH_UR_PK,

    /** Urdu pieces use ur-PK and Latin pieces use en-US, queued in order. */
    DUAL_LOCALE,
}

/**
 * Speaks a mixed Urdu and English line with Android's TextToSpeech engine.
 * Google Speech Services (com.google.android.tts) is preferred. The device engine is used if that package is absent.
 */
class BilingualTtsManager(
    context: Context,
    private val onReady: (urduAvailable: Boolean, engineLabel: String) -> Unit,
    private val onSpeakingChanged: (Boolean) -> Unit,
) : TextToSpeech.OnInitListener {

    private val appContext = context.applicationContext
    private var tts: TextToSpeech? = null
    private var ready = false
    private var triedDefaultEngine = false
    private var speechRate = 1f
    private var pending: (() -> Unit)? = null

    init {
        tts = TextToSpeech(appContext, this, GOOGLE_TTS)
    }

    override fun onInit(status: Int) {
        if (status != TextToSpeech.SUCCESS) {
            if (!triedDefaultEngine) {
                triedDefaultEngine = true
                tts?.shutdown()
                tts = TextToSpeech(appContext, this)
            } else {
                ready = false
                onReady(false, "Text-to-speech is unavailable")
            }
            return
        }
        ready = true
        val engine = tts ?: return
        engine.setOnUtteranceProgressListener(object : UtteranceProgressListener() {
            override fun onStart(utteranceId: String?) {
                onSpeakingChanged(true)
            }

            override fun onDone(utteranceId: String?) {
                if (utteranceId == LAST_UTTERANCE || utteranceId?.endsWith("-last") == true) {
                    onSpeakingChanged(false)
                }
            }

            @Deprecated("Deprecated in Java")
            override fun onError(utteranceId: String?) {
                onSpeakingChanged(false)
            }

            override fun onError(utteranceId: String?, errorCode: Int) {
                onSpeakingChanged(false)
            }
        })
        val urdu = engine.isLanguageAvailable(URDU)
        val urduReady = urdu >= TextToSpeech.LANG_AVAILABLE
        val label = if (triedDefaultEngine) "Device voice" else "Google Speech Services"
        onReady(urduReady, label)
        pending?.invoke()
        pending = null
    }

    fun setSpeechRate(rate: Float) {
        speechRate = rate.coerceIn(0.5f, 2f)
        tts?.setSpeechRate(speechRate)
    }

    fun speak(text: String, mode: TtsMode) {
        val spoken = text.trim()
        if (spoken.isEmpty()) return
        val action = {
            val engine = tts
            if (engine != null) {
                engine.setSpeechRate(speechRate)
                engine.stop()
                when (mode) {
                    TtsMode.SMOOTH_UR_PK -> speakSmooth(engine, spoken)
                    TtsMode.DUAL_LOCALE -> speakSegments(engine, spoken)
                }
            }
        }
        if (!ready) {
            pending = action
        } else {
            action()
        }
    }

    fun stop() {
        pending = null
        tts?.stop()
        onSpeakingChanged(false)
    }

    fun shutdown() {
        pending = null
        tts?.stop()
        tts?.shutdown()
        tts = null
        ready = false
    }

    private fun speakSmooth(engine: TextToSpeech, text: String) {
        engine.language = URDU
        engine.speak(text, TextToSpeech.QUEUE_FLUSH, null, LAST_UTTERANCE)
    }

    private fun speakSegments(engine: TextToSpeech, text: String) {
        val segments = ScriptSplitter.split(text)
        if (segments.isEmpty()) return
        segments.forEachIndexed { index, segment ->
            engine.language = if (segment.urdu) URDU else ENGLISH
            val queue = if (index == 0) TextToSpeech.QUEUE_FLUSH else TextToSpeech.QUEUE_ADD
            val id = if (index == segments.lastIndex) LAST_UTTERANCE else "seg-$index"
            engine.speak(segment.text, queue, null, id)
        }
    }

    companion object {
        private const val GOOGLE_TTS = "com.google.android.tts"
        private const val LAST_UTTERANCE = "hybrid-last"
        val URDU: Locale = Locale("ur", "PK")
        val ENGLISH: Locale = Locale.US
    }
}

data class ScriptSegment(val text: String, val urdu: Boolean)

object ScriptSplitter {
    fun split(text: String): List<ScriptSegment> {
        if (text.isBlank()) return emptyList()
        val parts = mutableListOf<ScriptSegment>()
        val buffer = StringBuilder()
        var urdu: Boolean? = null

        fun flush() {
            if (buffer.isNotEmpty() && urdu != null) {
                parts += ScriptSegment(buffer.toString(), urdu == true)
                buffer.clear()
            }
        }

        for (ch in text) {
            val kind = scriptOf(ch)
            when {
                kind == Script.OTHER -> buffer.append(ch)
                urdu == null -> {
                    urdu = kind == Script.URDU
                    buffer.append(ch)
                }
                (kind == Script.URDU) == urdu -> buffer.append(ch)
                else -> {
                    flush()
                    urdu = kind == Script.URDU
                    buffer.append(ch)
                }
            }
        }
        flush()
        return parts.filter { it.text.isNotBlank() }
    }

    private enum class Script { URDU, LATIN, OTHER }

    private fun scriptOf(ch: Char): Script = when {
        ch in '\u0600'..'\u06FF' ||
            ch in '\u0750'..'\u077F' ||
            ch in '\uFB50'..'\uFDFF' ||
            ch in '\uFE70'..'\uFEFF' -> Script.URDU
        ch.code < 128 && ch.isLetter() -> Script.LATIN
        else -> Script.OTHER
    }
}
