package com.sindhcs.crashcourse.data

import android.content.Context
import org.json.JSONObject

data class PageBlock(val type: String, val text: String, val golden: Boolean = false)

object PageRepository {

    @Volatile
    private var cached: Map<Int, List<PageBlock>>? = null

    @Volatile
    private var speech: Map<Int, String>? = null

    @Synchronized
    private fun load(context: Context): Map<Int, List<PageBlock>> {
        cached?.let { return it }
        val json = context.applicationContext.assets.open("course/pages.json")
            .bufferedReader().use { it.readText() }
        val root = JSONObject(json)
        val map = HashMap<Int, List<PageBlock>>()
        for (key in root.keys()) {
            val arr = root.getJSONArray(key)
            val blocks = ArrayList<PageBlock>(arr.length())
            for (i in 0 until arr.length()) {
                val o = arr.getJSONObject(i)
                blocks.add(PageBlock(o.getString("t"), o.getString("x"), o.optBoolean("g", false)))
            }
            map[key.toInt()] = blocks
        }
        cached = map
        return map
    }

    fun getBlocks(context: Context, bookletPage: Int): List<PageBlock> =
        load(context)[bookletPage].orEmpty()

    /** Spoken tutor text: Urdu description with {English exam terms}. */
    fun getSpeech(context: Context, bookletPage: Int): String {
        speech?.let { return it[bookletPage].orEmpty() }
        synchronized(this) {
            speech?.let { return it[bookletPage].orEmpty() }
            val json = context.applicationContext.assets.open("course/tts.json")
                .bufferedReader().use { it.readText() }
            val root = JSONObject(json)
            val map = HashMap<Int, String>(root.length())
            for (key in root.keys()) {
                map[key.toInt()] = root.getString(key)
            }
            speech = map
            return map[bookletPage].orEmpty()
        }
    }
}
