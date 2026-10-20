package com.hybridtts.urdu

import com.google.mlkit.common.model.DownloadConditions
import com.google.mlkit.nl.translate.TranslateLanguage
import com.google.mlkit.nl.translate.Translation
import com.google.mlkit.nl.translate.Translator
import com.google.mlkit.nl.translate.TranslatorOptions
import kotlinx.coroutines.tasks.await

/**
 * Turns English into Urdu while leaving chosen English words in Latin script.
 *
 * The sentence is masked with tokens such as [[0]] before ML Kit runs, then those
 * tokens are replaced with the original English words. If a model drops a token,
 * the same spans are translated as separate pieces and stitched back together.
 */
class HybridTranslator(
    private val geminiApiKey: String = "",
) {
    private val translator: Translator = Translation.getClient(
        TranslatorOptions.Builder()
            .setSourceLanguage(TranslateLanguage.ENGLISH)
            .setTargetLanguage(TranslateLanguage.URDU)
            .build(),
    )
    private val gemini = GeminiCodeSwitch(geminiApiKey)

    suspend fun ensureModel() {
        val conditions = DownloadConditions.Builder().build()
        translator.downloadModelIfNeeded(conditions).await()
    }

    suspend fun translate(
        text: String,
        customKeywords: List<String>,
        autoPreserve: Boolean,
    ): TranslationOutcome {
        val paragraphs = text.split('\n')
        val translated = StringBuilder()
        var usedSegments = false
        var usedGemini = false
        for ((index, paragraph) in paragraphs.withIndex()) {
            if (index > 0) translated.append('\n')
            if (paragraph.isBlank()) continue
            val piece = translateParagraph(paragraph, customKeywords, autoPreserve)
            translated.append(piece.text)
            usedSegments = usedSegments || piece.usedSegmentFallback
            usedGemini = usedGemini || piece.usedGemini
        }
        return TranslationOutcome(
            text = translated.toString().trim(),
            usedSegmentFallback = usedSegments,
            usedGemini = usedGemini,
        )
    }

    fun close() {
        translator.close()
    }

    private suspend fun translateParagraph(
        paragraph: String,
        customKeywords: List<String>,
        autoPreserve: Boolean,
    ): TranslationOutcome {
        val spans = KeywordMasker.preserveSpans(paragraph, customKeywords, autoPreserve)
        if (spans.isEmpty()) {
            return TranslationOutcome(translateRaw(paragraph), usedSegmentFallback = false, usedGemini = false)
        }
        val masked = KeywordMasker.mask(paragraph, spans)
        return try {
            val urdu = translateRaw(masked.maskedText)
            val restored = KeywordMasker.reinject(urdu, masked.tokens)
            if (restored != null) {
                TranslationOutcome(restored, usedSegmentFallback = false, usedGemini = false)
            } else {
                TranslationOutcome(
                    text = translateAroundSpans(paragraph, spans),
                    usedSegmentFallback = true,
                    usedGemini = false,
                )
            }
        } catch (mlKitError: Exception) {
            val smart = gemini.translate(paragraph, spans.map { it.original })
            if (smart != null) {
                TranslationOutcome(smart, usedSegmentFallback = false, usedGemini = true)
            } else {
                throw mlKitError
            }
        }
    }

    private suspend fun translateAroundSpans(text: String, spans: List<KeywordMasker.Span>): String {
        val sb = StringBuilder()
        var cursor = 0
        for (span in spans) {
            appendTranslatedGap(sb, text.substring(cursor, span.start))
            appendEnglishWord(sb, span.original)
            cursor = span.endExclusive
        }
        appendTranslatedGap(sb, text.substring(cursor))
        return sb.toString().replace(Regex("[ \\t]{2,}"), " ").trim()
    }

    private suspend fun appendTranslatedGap(sb: StringBuilder, gap: String) {
        if (gap.isBlank()) {
            if (gap.isNotEmpty() && sb.isNotEmpty() && !sb.last().isWhitespace()) sb.append(' ')
            return
        }
        val urdu = translateRaw(gap).trim()
        if (urdu.isEmpty()) return
        if (sb.isNotEmpty() && !sb.last().isWhitespace()) sb.append(' ')
        sb.append(urdu)
    }

    private fun appendEnglishWord(sb: StringBuilder, word: String) {
        if (sb.isNotEmpty() && !sb.last().isWhitespace()) sb.append(' ')
        sb.append(word)
    }

    private suspend fun translateRaw(text: String): String {
        val trimmed = text.trim()
        if (trimmed.isEmpty()) return ""
        return translator.translate(trimmed).await()
    }
}

data class TranslationOutcome(
    val text: String,
    val usedSegmentFallback: Boolean,
    val usedGemini: Boolean,
)

/**
 * Finds English words that must stay in Latin script, and hides them from the translator.
 */
object KeywordMasker {
    data class Span(val start: Int, val endExclusive: Int, val original: String)

    data class Masked(val maskedText: String, val tokens: List<String>)

    fun preserveSpans(text: String, customKeywords: List<String>, autoPreserve: Boolean): List<Span> {
        val found = mutableListOf<Span>()
        for (keyword in customKeywords) {
            val trimmed = keyword.trim()
            if (trimmed.isEmpty()) continue
            val pattern = Regex("\\b${Regex.escape(trimmed)}\\b", RegexOption.IGNORE_CASE)
            pattern.findAll(text).forEach { match ->
                found += Span(match.range.first, match.range.last + 1, match.value)
            }
        }
        if (autoPreserve) {
            found += quotedSpans(text)
            found += patternSpans(text, CAMEL)
            found += patternSpans(text, ACRONYM)
            found += capitalizedPhrases(text)
            found += singleCapitals(text)
        }
        return merge(found).filter { it.original.any { ch -> ch.isLetter() } }
    }

    fun mask(text: String, spans: List<Span>): Masked {
        val sb = StringBuilder()
        val tokens = mutableListOf<String>()
        var cursor = 0
        for (span in spans) {
            if (span.start < cursor || span.endExclusive > text.length) continue
            sb.append(text, cursor, span.start)
            sb.append("[[${tokens.size}]]")
            tokens += text.substring(span.start, span.endExclusive)
            cursor = span.endExclusive
        }
        if (cursor < text.length) sb.append(text, cursor, text.length)
        return Masked(sb.toString(), tokens)
    }

    /**
     * Puts the English words back. Returns null when the translator dropped a token,
     * so the caller can translate around the keywords instead.
     */
    fun reinject(translated: String, tokens: List<String>): String? {
        var out = translated
        for (index in tokens.indices.reversed()) {
            val loose = Regex("""\[\[\s*$index\s*]]""")
            if (!loose.containsMatchIn(out)) return null
            out = loose.replace(out, tokens[index])
        }
        return out
    }

    private fun quotedSpans(text: String): List<Span> {
        val spans = mutableListOf<Span>()
        val patterns = listOf(
            Regex("[\"“”']([^\"“”']+)[\"“”']"),
            Regex("\\*([^*]+)\\*"),
            Regex("`([^`]+)`"),
        )
        for (pattern in patterns) {
            pattern.findAll(text).forEach { match ->
                val inner = match.groups[1] ?: return@forEach
                spans += Span(inner.range.first, inner.range.last + 1, inner.value)
            }
        }
        return spans
    }

    private fun patternSpans(text: String, pattern: Regex): List<Span> =
        pattern.findAll(text).map { Span(it.range.first, it.range.last + 1, it.value) }.toList()

    private fun capitalizedPhrases(text: String): List<Span> =
        PHRASE.findAll(text).map { Span(it.range.first, it.range.last + 1, it.value) }.toList()

    private fun singleCapitals(text: String): List<Span> {
        val spans = mutableListOf<Span>()
        SINGLE.findAll(text).forEach { match ->
            if (isSentenceStart(text, match.range.first)) return@forEach
            spans += Span(match.range.first, match.range.last + 1, match.value)
        }
        return spans
    }

    private fun isSentenceStart(text: String, index: Int): Boolean {
        var cursor = index - 1
        while (cursor >= 0 && text[cursor].isWhitespace()) cursor--
        if (cursor < 0) return true
        return text[cursor] in ".!?"
    }

    private fun merge(spans: List<Span>): List<Span> {
        val sorted = spans
            .filter { it.endExclusive > it.start }
            .sortedWith(compareBy<Span> { it.start }.thenByDescending { it.endExclusive })
        val merged = mutableListOf<Span>()
        for (span in sorted) {
            val last = merged.lastOrNull()
            when {
                last == null -> merged += span
                span.start >= last.endExclusive -> merged += span
                span.endExclusive > last.endExclusive && span.start <= last.start ->
                    merged[merged.lastIndex] = span
            }
        }
        return merged
    }

    private val CAMEL = Regex("\\b[A-Za-z]*[a-z][A-Z][A-Za-z0-9]*\\b")
    private val ACRONYM = Regex("\\b[A-Z][A-Z0-9]{1,}\\b")
    private val PHRASE = Regex("\\b[A-Z][a-z0-9]+(?:\\s+[A-Z][a-z0-9]+)+\\b")
    private val SINGLE = Regex("\\b[A-Z][a-z0-9]{1,}\\b")
}
