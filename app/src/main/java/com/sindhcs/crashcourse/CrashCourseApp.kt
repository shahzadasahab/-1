package com.sindhcs.crashcourse

import android.app.Application
import com.sindhcs.crashcourse.util.LocaleHelper

class CrashCourseApp : Application() {
    override fun attachBaseContext(base: android.content.Context) {
        super.attachBaseContext(LocaleHelper.wrap(base))
    }
}
