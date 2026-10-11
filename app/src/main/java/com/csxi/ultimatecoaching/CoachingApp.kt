package com.csxi.ultimatecoaching

import android.app.Application
import com.csxi.ultimatecoaching.util.LocaleHelper

class CoachingApp : Application() {
    override fun attachBaseContext(base: android.content.Context) {
        super.attachBaseContext(LocaleHelper.wrap(base))
    }
}
