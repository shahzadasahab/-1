package com.sindhcs.crashcourse.util

import android.content.Context
import android.content.res.AssetManager
import android.media.AudioAttributes
import android.media.AudioFormat
import android.media.AudioTrack
import com.k2fsa.sherpa.onnx.OfflineTts
import com.k2fsa.sherpa.onnx.OfflineTtsConfig
import com.k2fsa.sherpa.onnx.OfflineTtsModelConfig
import com.k2fsa.sherpa.onnx.OfflineTtsVitsModelConfig
import java.io.File
import java.io.FileOutputStream
import java.util.concurrent.atomic.AtomicBoolean

/**
 * Bundled male Urdu teaching voice: Piper Fasih (ur_PK), for intermediate / HSSC students.
 * English exam terms are spoken by the same male teacher so the lesson stays one voice.
 */
class EmbeddedMaleVoice(context: Context) {

    private val app = context.applicationContext
    private val lock = Any()
    @Volatile private var tts: OfflineTts? = null
    @Volatile var ready: Boolean = false
        private set
    private val stopFlag = AtomicBoolean(false)
    private var track: AudioTrack? = null

    val label: String = "Embedded male tutor · Fasih (ur-PK)"

    fun load(): Boolean = synchronized(lock) {
        if (ready && tts != null) return true
        return runCatching {
            if (!assetExists("$ASSET_DIR/$MODEL")) return@runCatching false
            val espeak = copyEspeakData()
            val vits = OfflineTtsVitsModelConfig().apply {
                model = "$ASSET_DIR/$MODEL"
                tokens = "$ASSET_DIR/tokens.txt"
                lexicon = ""
                dataDir = espeak.absolutePath
            }
            val model = OfflineTtsModelConfig().apply {
                this.vits = vits
                numThreads = 2
                debug = false
                provider = "cpu"
            }
            val config = OfflineTtsConfig().apply { this.model = model }
            tts = OfflineTts(app.assets, config)
            ready = tts != null
            ready
        }.getOrDefault(false)
    }

    fun stop() {
        stopFlag.set(true)
        synchronized(lock) {
            runCatching { track?.pause() }
            runCatching { track?.stop() }
            runCatching { track?.release() }
            track = null
        }
    }

    fun release() {
        stop()
        synchronized(lock) {
            runCatching { tts?.release() }
            tts = null
            ready = false
        }
    }

    /** Synthesize and play on the calling thread. Returns false if stopped or failed. */
    fun speakBlocking(text: String, speed: Float): Boolean {
        val engine = tts ?: return false
        if (text.isBlank()) return true
        stopFlag.set(false)
        val audio = synchronized(lock) {
            runCatching { engine.generate(text, 0, speed.coerceIn(0.5f, 2.0f)) }.getOrNull()
        } ?: return false
        val samples = audio.samples
        if (samples.isEmpty()) return false
        return playBlocking(samples, audio.sampleRate)
    }

    private fun playBlocking(samples: FloatArray, sampleRate: Int): Boolean {
        val shorts = ShortArray(samples.size) { i ->
            (samples[i].coerceIn(-1f, 1f) * Short.MAX_VALUE).toInt().toShort()
        }
        val minBuf = AudioTrack.getMinBufferSize(
            sampleRate, AudioFormat.CHANNEL_OUT_MONO, AudioFormat.ENCODING_PCM_16BIT
        ).coerceAtLeast(4096)
        val created = AudioTrack.Builder()
            .setAudioAttributes(
                AudioAttributes.Builder()
                    .setUsage(AudioAttributes.USAGE_MEDIA)
                    .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
                    .build()
            )
            .setAudioFormat(
                AudioFormat.Builder()
                    .setEncoding(AudioFormat.ENCODING_PCM_16BIT)
                    .setSampleRate(sampleRate)
                    .setChannelMask(AudioFormat.CHANNEL_OUT_MONO)
                    .build()
            )
            .setBufferSizeInBytes(minBuf)
            .setTransferMode(AudioTrack.MODE_STREAM)
            .build()
        synchronized(lock) {
            track?.release()
            track = created
        }
        created.play()
        var offset = 0
        while (offset < shorts.size && !stopFlag.get()) {
            val written = created.write(shorts, offset, (shorts.size - offset).coerceAtMost(2048))
            if (written <= 0) break
            offset += written
        }
        if (!stopFlag.get()) {
            val remaining = ((shorts.size - created.playbackHeadPosition).coerceAtLeast(0) * 1000L / sampleRate) + 40
            var waited = 0L
            while (waited < remaining && !stopFlag.get() && created.playState == AudioTrack.PLAYSTATE_PLAYING) {
                Thread.sleep(20)
                waited += 20
            }
        }
        runCatching { created.stop() }
        runCatching { created.release() }
        synchronized(lock) { if (track === created) track = null }
        return !stopFlag.get()
    }

    private fun copyEspeakData(): File {
        val dest = File(app.filesDir, "tts/espeak-ng-data")
        val marker = File(dest, ".ok")
        if (marker.exists() && dest.isDirectory) return dest
        dest.deleteRecursively()
        copyAssetDir(app.assets, "$ASSET_DIR/espeak-ng-data", dest)
        marker.writeText("1")
        return dest
    }

    private fun copyAssetDir(assets: AssetManager, from: String, to: File) {
        val kids = assets.list(from) ?: return
        if (kids.isEmpty()) {
            to.parentFile?.mkdirs()
            assets.open(from).use { input ->
                FileOutputStream(to).use { output -> input.copyTo(output) }
            }
            return
        }
        to.mkdirs()
        for (name in kids) {
            copyAssetDir(assets, "$from/$name", File(to, name))
        }
    }

    private fun assetExists(path: String): Boolean =
        runCatching { app.assets.open(path).close(); true }.getOrDefault(false)

    companion object {
        const val ASSET_DIR = "tts/ur_male"
        const val MODEL = "ur_PK-fasih-medium.onnx"
    }
}
