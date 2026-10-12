package com.sindhcs.crashcourse.util

import android.content.Context
import android.content.res.Configuration
import java.util.Locale

object LocaleHelper {

    const val LANG_EN = "en"

    fun wrap(context: Context): Context {
        val locale = Locale.ENGLISH
        Locale.setDefault(locale)
        val config = Configuration(context.resources.configuration)
        config.setLocale(locale)
        config.setLayoutDirection(locale)
        return context.createConfigurationContext(config)
    }
}
