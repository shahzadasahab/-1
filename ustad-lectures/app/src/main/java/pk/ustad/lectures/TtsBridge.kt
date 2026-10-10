package pk.ustad.lectures

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.speech.tts.TextToSpeech
import android.speech.tts.UtteranceProgressListener
import android.webkit.JavascriptInterface
import org.json.JSONArray
import org.json.JSONObject
import java.util.Locale

/**
 * Bridges the lecture web UI to Android's TextToSpeech engine.
 *
 * Lectures are "Urdish": Urdu-script narration with English technical terms. A single
 * TTS voice cannot read both well, so the JS side splits every sentence into language
 * runs and this class speaks them one after another, switching the engine language
 * between runs.
 */
class TtsBridge(
    private val context: Context,
    private val emit: (String) -> Unit,
) {
    private val main = Handler(Looper.getMainLooper())
    private var tts: TextToSpeech? = null
    @Volatile private var ready = false
    @Volatile private var initFailed = false

    @Volatile private var urLocale: Locale? = null
    @Volatile private var enLocale: Locale? = null
    private var currentLang: String? = null

    private var job = 0
    private var items: List<Item> = emptyList()
    private var itemIdx = 0
    private var segIdx = 0
    private var rate = 0.9f
    private var pendingSpeak: (() -> Unit)? = null

    private class Seg(val lang: String, val text: String)
    private class Item(val id: Int, val segs: List<Seg>)

    init {
        main.post { createEngine() }
    }

    private fun createEngine() {
        tts = TextToSpeech(context.applicationContext) { status ->
            main.post {
                if (status == TextToSpeech.SUCCESS) {
                    resolveLocales()
                    ready = true
                    tts?.setOnUtteranceProgressListener(listener)
                    pendingSpeak?.invoke()
                    pendingSpeak = null
                } else {
                    initFailed = true
                    pendingSpeak = null
                    emit("window.__tts && __tts.onNative(" + JSONObject().put("type", "error")
                        .put("job", job).put("msg", "init").toString() + ")")
                }
            }
        }
    }

    private fun supported(l: Locale): Boolean {
        val r = tts?.isLanguageAvailable(l) ?: TextToSpeech.LANG_NOT_SUPPORTED
        return r >= TextToSpeech.LANG_AVAILABLE
    }

    private fun resolveLocales() {
        urLocale = listOf(Locale("ur", "PK"), Locale("ur", "IN"), Locale("ur"))
            .firstOrNull { supported(it) }
        enLocale = listOf(Locale("en", "IN"), Locale("en", "PK"), Locale.US, Locale.UK, Locale.ENGLISH)
            .firstOrNull { supported(it) }
    }

    private val listener = object : UtteranceProgressListener() {
        override fun onStart(utteranceId: String?) {}

        override fun onDone(utteranceId: String?) {
            val parts = utteranceId?.split(":") ?: return
            if (parts.size < 3 || parts[0].toIntOrNull() != job) return
            main.post { advance(job) }
        }

        @Deprecated("Deprecated in Java")
        override fun onError(utteranceId: String?) {
            val parts = utteranceId?.split(":") ?: return
            if (parts.size < 3 || parts[0].toIntOrNull() != job) return
            main.post { advance(job) }
        }
    }

    private fun event(type: String, id: Int = -1, msg: String? = null) {
        val o = JSONObject().put("type", type).put("job", job).put("id", id)
        if (msg != null) o.put("msg", msg)
        emit("window.__tts && __tts.onNative(" + o.toString() + ")")
    }

    private fun advance(forJob: Int) {
        if (forJob != job) return
        segIdx++
        playCurrent()
    }

    private fun playCurrent() {
        val engine = tts ?: return
        while (true) {
            if (itemIdx >= items.size) {
                event("done")
                return
            }
            val item = items[itemIdx]
            if (segIdx == 0) event("start", item.id)
            if (segIdx >= item.segs.size) {
                event("end", item.id)
                itemIdx++
                segIdx = 0
                continue
            }
            val seg = item.segs[segIdx]
            val locale = if (seg.lang == "ur") urLocale else enLocale
            if (locale == null) {
                if (seg.lang == "ur") event("missing", item.id, "ur")
                segIdx++
                continue
            }
            if (currentLang != seg.lang) {
                engine.language = locale
                currentLang = seg.lang
            }
            engine.setSpeechRate(rate)
            val params = Bundle()
            val uid = "$job:${item.id}:$segIdx"
            val res = engine.speak(seg.text, TextToSpeech.QUEUE_FLUSH, params, uid)
            if (res != TextToSpeech.SUCCESS) {
                segIdx++
                continue
            }
            return
        }
    }

    @JavascriptInterface
    fun status(): String {
        val o = JSONObject()
        o.put("native", true)
        o.put("ready", ready)
        o.put("failed", initFailed)
        if (ready) {
            o.put("ur", urLocale != null)
            o.put("en", enLocale != null)
            o.put("engine", tts?.defaultEngine ?: "")
        }
        return o.toString()
    }

    @JavascriptInterface
    fun refresh() {
        main.post {
            if (ready) resolveLocales()
        }
    }

    @JavascriptInterface
    fun speak(jobId: Int, itemsJson: String, speechRate: Float) {
        main.post {
            val parsed = try {
                parse(itemsJson)
            } catch (e: Exception) {
                emptyList()
            }
            val start = {
                job = jobId
                items = parsed
                itemIdx = 0
                segIdx = 0
                rate = speechRate
                currentLang = null
                tts?.stop()
                playCurrent()
            }
            if (ready) start() else if (initFailed) event("error", msg = "init") else pendingSpeak = start
        }
    }

    private fun parse(json: String): List<Item> {
        val arr = JSONArray(json)
        val out = ArrayList<Item>(arr.length())
        for (i in 0 until arr.length()) {
            val o = arr.getJSONObject(i)
            val segsJson = o.getJSONArray("segs")
            val segs = ArrayList<Seg>(segsJson.length())
            for (j in 0 until segsJson.length()) {
                val s = segsJson.getJSONObject(j)
                segs.add(Seg(s.getString("l"), s.getString("t")))
            }
            out.add(Item(o.getInt("id"), segs))
        }
        return out
    }

    @JavascriptInterface
    fun stop() {
        main.post {
            job++
            items = emptyList()
            pendingSpeak = null
            tts?.stop()
        }
    }

    @JavascriptInterface
    fun openVoiceSettings() {
        main.post {
            val intents = listOf(
                Intent("com.android.settings.TTS_SETTINGS"),
                Intent("android.settings.SETTINGS"),
            )
            for (i in intents) {
                try {
                    i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                    context.startActivity(i)
                    return@post
                } catch (_: Exception) {
                }
            }
        }
    }

    @JavascriptInterface
    fun installVoiceData() {
        main.post {
            try {
                val i = Intent(TextToSpeech.Engine.ACTION_INSTALL_TTS_DATA)
                i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                context.startActivity(i)
            } catch (_: Exception) {
                openVoiceSettings()
            }
        }
    }

    fun shutdown() {
        job++
        tts?.stop()
        tts?.shutdown()
        tts = null
    }

    fun pause() {
        main.post {
            job++
            items = emptyList()
            tts?.stop()
        }
    }
}
