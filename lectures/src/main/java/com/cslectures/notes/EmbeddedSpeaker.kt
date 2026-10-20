package com.cslectures.notes

import android.content.Context
import android.media.AudioAttributes
import android.media.AudioFormat
import android.media.AudioTrack
import android.util.Log
import com.k2fsa.sherpa.onnx.OfflineTts
import com.k2fsa.sherpa.onnx.OfflineTtsConfig
import com.k2fsa.sherpa.onnx.OfflineTtsModelConfig
import com.k2fsa.sherpa.onnx.OfflineTtsVitsModelConfig
import java.io.File
import java.util.concurrent.Executors
import java.util.concurrent.atomic.AtomicInteger

/**
 * Offline speech using the Piper Amy int8 voice stored in the APK.
 * espeak-ng phoneme data is copied out of assets once, because the
 * synthesizer opens those files from a real directory.
 */
class EmbeddedSpeaker(private val context: Context) {
    interface Listener {
        fun onEngineReady(ready: Boolean, message: String)
        fun onPlayback(speaking: Boolean, paused: Boolean)
        fun onBlock(index: Int)
    }

    @Volatile
    var listener: Listener? = null

    @Volatile
    private var ready = false

    @Volatile
    private var failed = false

    @Volatile
    private var paused = false

    private val generation = AtomicInteger(0)
    private val executor = Executors.newSingleThreadExecutor()
    private val main = android.os.Handler(android.os.Looper.getMainLooper())
    private var tts: OfflineTts? = null
    private var track: AudioTrack? = null

    fun prepare() {
        executor.execute { ensureEngine() }
    }

    fun speak(blocks: List<Block>, startIndex: Int, speed: Float) {
        val id = generation.incrementAndGet()
        paused = false
        executor.execute {
            if (!ensureEngine()) return@execute
            main.post { listener?.onPlayback(speaking = true, paused = false) }
            val engine = tts ?: return@execute
            val from = startIndex.coerceIn(0, blocks.lastIndex.coerceAtLeast(0))
            for (index in from until blocks.size) {
                if (generation.get() != id) break
                val speech = blocks[index].speech.trim()
                if (speech.isEmpty()) continue
                main.post {
                    if (generation.get() == id) listener?.onBlock(index)
                }
                for (chunk in chunk(speech)) {
                    if (generation.get() != id) break
                    waitWhilePaused(id)
                    if (generation.get() != id) break
                    engine.generateWithCallback(chunk, 0, speed) { samples ->
                        writeSamples(samples, id)
                    }
                }
            }
            if (generation.get() == id) {
                track?.stop()
                main.post { listener?.onPlayback(speaking = false, paused = false) }
            }
        }
    }

    fun pause() {
        paused = true
        track?.pause()
        main.post { listener?.onPlayback(speaking = true, paused = true) }
    }

    fun resume() {
        paused = false
        if (track?.playState != AudioTrack.PLAYSTATE_PLAYING) {
            track?.play()
        }
        main.post { listener?.onPlayback(speaking = true, paused = false) }
    }

    fun stop() {
        generation.incrementAndGet()
        paused = false
        executor.execute {
            track?.pause()
            track?.flush()
            main.post { listener?.onPlayback(speaking = false, paused = false) }
        }
    }

    fun release() {
        generation.incrementAndGet()
        executor.execute {
            track?.release()
            track = null
            tts?.release()
            tts = null
            ready = false
        }
    }

    private fun ensureEngine(): Boolean {
        if (ready && tts != null) return true
        if (failed) return false
        return try {
            val dataDir = prepareEspeakData()
            val config = OfflineTtsConfig(
                model = OfflineTtsModelConfig(
                    vits = OfflineTtsVitsModelConfig(
                        model = "tts/en_US-amy-low.onnx",
                        tokens = "tts/tokens.txt",
                        dataDir = dataDir,
                        lexicon = "",
                    ),
                    numThreads = 2,
                    debug = false,
                    provider = "cpu",
                ),
            )
            val engine = OfflineTts(assetManager = context.assets, config = config)
            tts = engine
            track = buildTrack(engine.sampleRate())
            ready = true
            main.post { listener?.onEngineReady(true, "Embedded voice ready") }
            true
        } catch (error: Throwable) {
            Log.e(TAG, "Failed to start embedded TTS", error)
            failed = true
            ready = false
            main.post {
                listener?.onEngineReady(false, error.message ?: "The embedded voice failed to start")
            }
            false
        }
    }

    private fun buildTrack(sampleRate: Int): AudioTrack {
        val encoding = AudioFormat.ENCODING_PCM_FLOAT
        var buffer = AudioTrack.getMinBufferSize(
            sampleRate,
            AudioFormat.CHANNEL_OUT_MONO,
            encoding,
        )
        if (buffer <= 0) buffer = sampleRate
        val attributes = AudioAttributes.Builder()
            .setUsage(AudioAttributes.USAGE_MEDIA)
            .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
            .build()
        val format = AudioFormat.Builder()
            .setSampleRate(sampleRate)
            .setEncoding(encoding)
            .setChannelMask(AudioFormat.CHANNEL_OUT_MONO)
            .build()
        return AudioTrack.Builder()
            .setAudioAttributes(attributes)
            .setAudioFormat(format)
            .setBufferSizeInBytes(buffer * 2)
            .setTransferMode(AudioTrack.MODE_STREAM)
            .build()
    }

    private fun writeSamples(samples: FloatArray, id: Int): Int {
        if (generation.get() != id) return 0
        waitWhilePaused(id)
        if (generation.get() != id) return 0
        val audio = track ?: return 0
        if (audio.playState != AudioTrack.PLAYSTATE_PLAYING) {
            audio.play()
        }
        val written = audio.write(samples, 0, samples.size, AudioTrack.WRITE_BLOCKING)
        return if (written < 0 || generation.get() != id) 0 else 1
    }

    private fun waitWhilePaused(id: Int) {
        while (paused && generation.get() == id) {
            track?.pause()
            try {
                Thread.sleep(40)
            } catch (_: InterruptedException) {
                return
            }
        }
    }

    private fun prepareEspeakData(): String {
        val dest = File(context.filesDir, "espeak-ng-data")
        val stamp = File(dest, ".stamp")
        if (stamp.exists() && stamp.readText() == STAMP) {
            return dest.absolutePath
        }
        dest.deleteRecursively()
        copyAssetDir("tts/espeak-ng-data", dest)
        stamp.writeText(STAMP)
        return dest.absolutePath
    }

    private fun copyAssetDir(assetPath: String, dest: File) {
        val children = context.assets.list(assetPath).orEmpty()
        if (children.isEmpty()) {
            dest.parentFile?.mkdirs()
            context.assets.open(assetPath).use { input ->
                dest.outputStream().use { output -> input.copyTo(output) }
            }
            return
        }
        dest.mkdirs()
        for (child in children) {
            copyAssetDir("$assetPath/$child", File(dest, child))
        }
    }

    private fun chunk(text: String): List<String> {
        val sentences = text.split(Regex("(?<=[.!?])\\s+"))
        val chunks = mutableListOf<String>()
        val buffer = StringBuilder()
        for (sentence in sentences) {
            if (buffer.isNotEmpty() && buffer.length + sentence.length > 380) {
                chunks += buffer.toString().trim()
                buffer.clear()
            }
            if (buffer.isNotEmpty()) buffer.append(' ')
            buffer.append(sentence)
        }
        if (buffer.isNotBlank()) chunks += buffer.toString().trim()
        return chunks.ifEmpty { listOf(text) }
    }

    companion object {
        private const val TAG = "EmbeddedSpeaker"
        private const val STAMP = "amy-int8-en-1"
    }
}
