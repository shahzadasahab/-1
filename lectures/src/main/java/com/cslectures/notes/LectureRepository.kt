package com.cslectures.notes

import android.content.Context
import org.json.JSONObject

object LectureRepository {
    @Volatile
    private var cached: List<Lecture>? = null

    fun lectures(context: Context): List<Lecture> {
        cached?.let { return it }
        val json = context.assets.open("lectures.json").bufferedReader().use { it.readText() }
        val root = JSONObject(json)
        val array = root.getJSONArray("lectures")
        val lectures = buildList {
            for (i in 0 until array.length()) {
                val item = array.getJSONObject(i)
                val blocksJson = item.getJSONArray("blocks")
                val blocks = buildList {
                    for (b in 0 until blocksJson.length()) {
                        val block = blocksJson.getJSONObject(b)
                        add(
                            Block(
                                kind = block.getString("kind"),
                                display = block.getString("display"),
                                speech = block.getString("speech"),
                            )
                        )
                    }
                }
                add(
                    Lecture(
                        id = item.getString("id"),
                        kicker = item.getString("kicker"),
                        title = item.getString("title"),
                        deck = item.optString("deck"),
                        blocks = blocks,
                    )
                )
            }
        }
        cached = lectures
        return lectures
    }

    fun find(context: Context, id: String): Lecture? =
        lectures(context).firstOrNull { it.id == id }
}
