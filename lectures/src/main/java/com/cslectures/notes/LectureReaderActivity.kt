package com.cslectures.notes

import android.os.Bundle
import android.view.LayoutInflater
import android.view.ViewGroup
import android.view.WindowManager
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.cslectures.notes.databinding.ActivityLectureReaderBinding
import com.cslectures.notes.databinding.ItemBlockBinding

class LectureReaderActivity : AppCompatActivity(), EmbeddedSpeaker.Listener {
    private lateinit var binding: ActivityLectureReaderBinding
    private lateinit var lecture: Lecture
    private lateinit var speaker: EmbeddedSpeaker
    private var startIndex = 0
    private var activeIndex = -1
    private var speedIndex = 1
    private val speeds = floatArrayOf(0.9f, 1.0f, 1.15f)
    private val speedLabels = arrayOf("0.9×", "1.0×", "1.15×")

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val found = LectureRepository.find(this, intent.getStringExtra(EXTRA_ID).orEmpty())
        if (found == null) {
            finish()
            return
        }
        lecture = found
        speaker = (application as LectureApp).speaker
        binding = ActivityLectureReaderBinding.inflate(layoutInflater)
        setContentView(binding.root)
        binding.toolbar.title = lecture.title
        binding.toolbar.subtitle = lecture.kicker
        binding.toolbar.setNavigationOnClickListener {
            speaker.stop()
            finish()
        }
        val adapter = BlockAdapter(lecture.blocks) { index ->
            val previous = startIndex
            startIndex = index
            if (previous != index) {
                binding.blockList.adapter?.notifyItemChanged(previous)
                binding.blockList.adapter?.notifyItemChanged(index)
            }
            binding.voiceStatus.text = getString(R.string.starts_here, index + 1)
        }
        binding.blockList.layoutManager = LinearLayoutManager(this)
        binding.blockList.adapter = adapter
        binding.play.setOnClickListener {
            speaker.speak(lecture.blocks, startIndex, speeds[speedIndex])
        }
        binding.pause.setOnClickListener { speaker.pause() }
        binding.resume.setOnClickListener { speaker.resume() }
        binding.stop.setOnClickListener {
            speaker.stop()
            window.clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
        }
        binding.speed.setOnClickListener {
            speedIndex = (speedIndex + 1) % speeds.size
            binding.speed.text = getString(R.string.speed_label, speedLabels[speedIndex])
        }
        binding.speed.text = getString(R.string.speed_label, speedLabels[speedIndex])
        speaker.listener = this
    }

    override fun onResume() {
        super.onResume()
        speaker.listener = this
    }

    override fun onDestroy() {
        if (isFinishing) speaker.stop()
        super.onDestroy()
    }

    override fun onEngineReady(ready: Boolean, message: String) {
        binding.voiceStatus.text = if (ready) {
            getString(R.string.voice_ready)
        } else {
            getString(R.string.voice_failed, message)
        }
        binding.play.isEnabled = ready
    }

    override fun onPlayback(speaking: Boolean, paused: Boolean) {
        if (speaking) {
            window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
            binding.voiceStatus.text = if (paused) {
                getString(R.string.paused)
            } else {
                getString(R.string.speaking)
            }
        } else {
            window.clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
            binding.voiceStatus.text = getString(R.string.voice_ready)
            setActive(-1)
        }
        binding.pause.isEnabled = speaking && !paused
        binding.resume.isEnabled = speaking && paused
    }

    override fun onBlock(index: Int) {
        setActive(index)
        binding.blockList.smoothScrollToPosition(index)
    }

    private fun setActive(index: Int) {
        val previous = activeIndex
        activeIndex = index
        val adapter = binding.blockList.adapter ?: return
        if (previous >= 0) adapter.notifyItemChanged(previous)
        if (index >= 0) adapter.notifyItemChanged(index)
    }

    private inner class BlockAdapter(
        private val blocks: List<Block>,
        private val onPick: (Int) -> Unit,
    ) : RecyclerView.Adapter<BlockAdapter.Holder>() {
        override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): Holder {
            val binding = ItemBlockBinding.inflate(LayoutInflater.from(parent.context), parent, false)
            return Holder(binding)
        }

        override fun onBindViewHolder(holder: Holder, position: Int) {
            val block = blocks[position]
            holder.binding.text.text = block.display
            val context = holder.itemView.context
            val speaking = position == activeIndex
            val picked = position == startIndex && activeIndex < 0
            holder.binding.text.setBackgroundColor(
                ContextCompat.getColor(
                    context,
                    when {
                        speaking -> R.color.speaking
                        picked -> R.color.picked
                        block.kind == "code" -> R.color.code_bg
                        block.kind == "note" -> R.color.note_bg
                        else -> android.R.color.transparent
                    },
                )
            )
            holder.binding.text.setTextAppearance(
                when (block.kind) {
                    "h" -> R.style.BlockHeading
                    "code" -> R.style.BlockCode
                    "caption" -> R.style.BlockCaption
                    else -> R.style.BlockBody
                }
            )
            holder.binding.root.setOnClickListener {
                val index = holder.bindingAdapterPosition
                if (index != RecyclerView.NO_POSITION) onPick(index)
            }
            holder.binding.root.contentDescription = block.speech
        }

        override fun getItemCount(): Int = blocks.size

        inner class Holder(val binding: ItemBlockBinding) : RecyclerView.ViewHolder(binding.root)
    }

    companion object {
        const val EXTRA_ID = "lecture_id"
    }
}
