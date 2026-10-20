package com.cslectures.notes

import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.cslectures.notes.databinding.ActivityLectureListBinding
import com.cslectures.notes.databinding.ItemLectureBinding

class LectureListActivity : AppCompatActivity(), EmbeddedSpeaker.Listener {
    private lateinit var binding: ActivityLectureListBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityLectureListBinding.inflate(layoutInflater)
        setContentView(binding.root)
        val lectures = LectureRepository.lectures(this)
        binding.lectureList.layoutManager = LinearLayoutManager(this)
        binding.lectureList.adapter = LectureAdapter(lectures) { lecture ->
            startActivity(
                Intent(this, LectureReaderActivity::class.java)
                    .putExtra(LectureReaderActivity.EXTRA_ID, lecture.id)
            )
        }
        val app = application as LectureApp
        app.speaker.listener = this
    }

    override fun onResume() {
        super.onResume()
        (application as LectureApp).speaker.listener = this
    }

    override fun onEngineReady(ready: Boolean, message: String) {
        binding.voiceStatus.text = if (ready) {
            getString(R.string.voice_ready)
        } else {
            getString(R.string.voice_failed, message)
        }
    }

    override fun onPlayback(speaking: Boolean, paused: Boolean) = Unit

    override fun onBlock(index: Int) = Unit

    private class LectureAdapter(
        private val lectures: List<Lecture>,
        private val onClick: (Lecture) -> Unit,
    ) : RecyclerView.Adapter<LectureAdapter.Holder>() {
        override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): Holder {
            val binding = ItemLectureBinding.inflate(LayoutInflater.from(parent.context), parent, false)
            return Holder(binding)
        }

        override fun onBindViewHolder(holder: Holder, position: Int) {
            val lecture = lectures[position]
            holder.binding.kicker.text = lecture.kicker
            holder.binding.title.text = lecture.title
            holder.binding.deck.text = lecture.deck
            holder.binding.root.setOnClickListener { onClick(lecture) }
        }

        override fun getItemCount(): Int = lectures.size

        class Holder(val binding: ItemLectureBinding) : RecyclerView.ViewHolder(binding.root)
    }
}
