package com.sindhcs.crashcourse.util

import android.content.Context
import android.content.res.Configuration
import java.util.Locale

object LocaleHelper {

    private const val PREFS = "cs_crash_prefs"
    private const val KEY_LANGUAGE = "language"

    const val LANG_EN = "en"
    const val LANG_UR = "ur"

    fun getLanguage(context: Context): String {
        val prefs = context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
        return prefs.getString(KEY_LANGUAGE, LANG_UR) ?: LANG_UR
    }

    fun setLanguage(context: Context, language: String) {
        context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
            .edit()
            .putString(KEY_LANGUAGE, language)
            .apply()
    }

    fun wrap(context: Context): Context {
        val language = getLanguage(context)
        val locale = if (language == LANG_UR) Locale("ur", "PK") else Locale.ENGLISH
        Locale.setDefault(locale)
        val config = Configuration(context.resources.configuration)
        config.setLocale(locale)
        config.setLayoutDirection(locale)
        return context.createConfigurationContext(config)
    }

    fun isUrdu(context: Context): Boolean = getLanguage(context) == LANG_UR
}
