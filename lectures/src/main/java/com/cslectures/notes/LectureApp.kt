package com.cslectures.notes

import android.app.Application

class LectureApp : Application() {
    lateinit var speaker: EmbeddedSpeaker
        private set

    override fun onCreate() {
        super.onCreate()
        speaker = EmbeddedSpeaker(this)
        speaker.prepare()
    }
}
