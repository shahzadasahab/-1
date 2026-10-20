package com.hybridtts.urdu

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

class KeywordMaskerTest {
    @Test
    fun masksACapitalizedPhraseAndRestoresIt() {
        val text = "Today we will study Artificial Intelligence."
        val spans = KeywordMasker.preserveSpans(text, emptyList(), autoPreserve = true)
        assertEquals(listOf("Artificial Intelligence"), spans.map { it.original })

        val masked = KeywordMasker.mask(text, spans)
        assertEquals("Today we will study [[0]].", masked.maskedText)

        val restored = KeywordMasker.reinject("آج ہم [[0]] کے بارے میں پڑھیں گے۔", masked.tokens)
        assertEquals("آج ہم Artificial Intelligence کے بارے میں پڑھیں گے۔", restored)
    }

    @Test
    fun keepsACustomWordAndAnAcronym() {
        val text = "Python uses an API for TTS."
        val spans = KeywordMasker.preserveSpans(text, listOf("Python"), autoPreserve = true)
        assertEquals(listOf("Python", "API", "TTS"), spans.map { it.original })
    }

    @Test
    fun doesNotKeepASentenceStarter() {
        val text = "Today the class begins."
        val spans = KeywordMasker.preserveSpans(text, emptyList(), autoPreserve = true)
        assertTrue(spans.isEmpty())
    }

    @Test
    fun keepsQuotedAndStarredWords() {
        val text = "Save the \"cache\" and mark *batch* as done."
        val spans = KeywordMasker.preserveSpans(text, emptyList(), autoPreserve = true)
        assertEquals(listOf("cache", "batch"), spans.map { it.original })
    }

    @Test
    fun reinjectFailsWhenATokenDisappears() {
        assertNull(KeywordMasker.reinject("آج ہم پڑھیں گے", listOf("Python")))
    }

    @Test
    fun splitsMixedScriptForTheDualVoice() {
        val segments = ScriptSplitter.split("آج ہم Artificial Intelligence پڑھیں گے")
        assertEquals(
            listOf(true, false, true),
            segments.map { it.urdu },
        )
        assertEquals("Artificial Intelligence", segments[1].text.trim())
    }
}
