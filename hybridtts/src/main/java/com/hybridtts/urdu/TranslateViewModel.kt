package com.hybridtts.urdu

import android.app.Application
import android.content.ActivityNotFoundException
import android.content.Intent
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class TranslateViewModel(application: Application) : AndroidViewModel(application) {
    private val translator = HybridTranslator(BuildConfig.GEMINI_API_KEY)
    private val tts = BilingualTtsManager(
        context = application,
        onReady = { urduReady, engineLabel ->
            _urduVoiceMissing.value = !urduReady
            _voiceLabel.value = if (urduReady) {
                "$engineLabel · ur-PK"
            } else {
                "$engineLabel · Urdu voice pack missing"
            }
        },
        onSpeakingChanged = { speaking -> _speaking.value = speaking },
    )

    private val _input = MutableStateFlow("")
    val input: StateFlow<String> = _input.asStateFlow()

    private val _keywords = MutableStateFlow("")
    val keywords: StateFlow<String> = _keywords.asStateFlow()

    private val _autoPreserve = MutableStateFlow(true)
    val autoPreserve: StateFlow<Boolean> = _autoPreserve.asStateFlow()

    private val _result = MutableStateFlow("")
    val result: StateFlow<String> = _result.asStateFlow()

    private val _status = MutableStateFlow("The Urdu model downloads once, the first time you translate.")
    val status: StateFlow<String> = _status.asStateFlow()

    private val _busy = MutableStateFlow(false)
    val busy: StateFlow<Boolean> = _busy.asStateFlow()

    private val _downloading = MutableStateFlow(false)
    val downloading: StateFlow<Boolean> = _downloading.asStateFlow()

    private val _speechRate = MutableStateFlow(1f)
    val speechRate: StateFlow<Float> = _speechRate.asStateFlow()

    private val _smoothVoice = MutableStateFlow(true)
    val smoothVoice: StateFlow<Boolean> = _smoothVoice.asStateFlow()

    private val _speaking = MutableStateFlow(false)
    val speaking: StateFlow<Boolean> = _speaking.asStateFlow()

    private val _urduVoiceMissing = MutableStateFlow(false)
    val urduVoiceMissing: StateFlow<Boolean> = _urduVoiceMissing.asStateFlow()

    private val _voiceLabel = MutableStateFlow("Starting voice…")
    val voiceLabel: StateFlow<String> = _voiceLabel.asStateFlow()

    fun setInput(value: String) {
        _input.value = value
    }

    fun setKeywords(value: String) {
        _keywords.value = value
    }

    fun setAutoPreserve(value: Boolean) {
        _autoPreserve.value = value
    }

    fun setSpeechRate(value: Float) {
        _speechRate.value = value
        tts.setSpeechRate(value)
    }

    fun setSmoothVoice(value: Boolean) {
        _smoothVoice.value = value
    }

    fun translateAndSpeak() {
        val source = _input.value.trim()
        if (source.isEmpty()) {
            _status.value = "Enter an English sentence first."
            return
        }
        viewModelScope.launch {
            _busy.value = true
            _downloading.value = true
            _status.value = "Downloading the Urdu model if it is not on the phone yet…"
            try {
                translator.ensureModel()
                _downloading.value = false
                _status.value = "Translating…"
                val outcome = translator.translate(
                    text = source,
                    customKeywords = _keywords.value.split(','),
                    autoPreserve = _autoPreserve.value,
                )
                _result.value = outcome.text
                _status.value = when {
                    outcome.usedGemini -> "Translated with the Gemini fallback. English terms stayed in Latin script."
                    outcome.usedSegmentFallback -> "Translated in pieces so the English terms were not rewritten."
                    else -> "Urdu sentence ready. English terms were put back in."
                }
                speakCurrent()
            } catch (error: Exception) {
                _downloading.value = false
                _status.value = error.message?.takeIf { it.isNotBlank() }
                    ?: "Translation failed. Check the connection and try again."
            } finally {
                _busy.value = false
                _downloading.value = false
            }
        }
    }

    fun play() {
        if (_result.value.isBlank()) {
            _status.value = "Translate a sentence before playing it."
            return
        }
        speakCurrent()
    }

    fun stop() {
        tts.stop()
    }

    fun openTtsSettings() {
        val context = getApplication<Application>()
        val intent = Intent("com.android.settings.TTS_SETTINGS").addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        try {
            context.startActivity(intent)
        } catch (_: ActivityNotFoundException) {
            _status.value = "This phone has no text-to-speech settings screen."
        }
    }

    override fun onCleared() {
        tts.shutdown()
        translator.close()
        super.onCleared()
    }

    private fun speakCurrent() {
        tts.setSpeechRate(_speechRate.value)
        val mode = if (_smoothVoice.value) TtsMode.SMOOTH_UR_PK else TtsMode.DUAL_LOCALE
        tts.speak(_result.value, mode)
    }
}
