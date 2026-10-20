package com.hybridtts.urdu

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
import java.net.URLEncoder

/**
 * Used only when on-device translation fails and a Gemini key is present in local.properties.
 * The key is never required for the app to run.
 */
class GeminiCodeSwitch(private val apiKey: String) {
    suspend fun translate(english: String, keepInEnglish: List<String>): String? = withContext(Dispatchers.IO) {
        if (apiKey.isBlank()) return@withContext null
        val keep = keepInEnglish.distinct().joinToString(", ").ifBlank { "(none)" }
        val prompt = """
            Translate this English into natural Pakistani Urdu.
            Keep every one of these words exactly as written, in Latin script, inside the Urdu sentence: $keep.
            Do not add notes. Return only the mixed Urdu sentence.
            English:
            $english
        """.trimIndent()
        val endpoint = "$ENDPOINT?key=${URLEncoder.encode(apiKey, "UTF-8")}"
        val connection = (URL(endpoint).openConnection() as HttpURLConnection).apply {
            requestMethod = "POST"
            connectTimeout = 20_000
            readTimeout = 20_000
            doOutput = true
            setRequestProperty("Content-Type", "application/json")
        }
        try {
            val body = JSONObject()
                .put(
                    "contents",
                    org.json.JSONArray().put(
                        JSONObject().put(
                            "parts",
                            org.json.JSONArray().put(JSONObject().put("text", prompt)),
                        ),
                    ),
                )
            connection.outputStream.use { it.write(body.toString().toByteArray()) }
            val code = connection.responseCode
            val stream = if (code in 200..299) connection.inputStream else connection.errorStream
            val response = stream.bufferedReader().use { it.readText() }
            if (code !in 200..299) return@withContext null
            JSONObject(response)
                .getJSONArray("candidates")
                .getJSONObject(0)
                .getJSONObject("content")
                .getJSONArray("parts")
                .getJSONObject(0)
                .getString("text")
                .trim()
                .ifBlank { null }
        } catch (_: Exception) {
            null
        } finally {
            connection.disconnect()
        }
    }

    companion object {
        private const val ENDPOINT =
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    }
}
