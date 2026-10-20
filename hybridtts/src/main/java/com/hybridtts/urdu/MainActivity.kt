package com.hybridtts.urdu

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.FilterChip
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Slider
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.style.TextDirection
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import java.util.Locale
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import com.hybridtts.urdu.ui.HybridUrduTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            HybridUrduTheme {
                val model: TranslateViewModel = viewModel()
                TranslateScreen(model)
            }
        }
    }
}

@Composable
private fun TranslateScreen(model: TranslateViewModel) {
    val input by model.input.collectAsStateWithLifecycle()
    val keywords by model.keywords.collectAsStateWithLifecycle()
    val autoPreserve by model.autoPreserve.collectAsStateWithLifecycle()
    val result by model.result.collectAsStateWithLifecycle()
    val status by model.status.collectAsStateWithLifecycle()
    val busy by model.busy.collectAsStateWithLifecycle()
    val downloading by model.downloading.collectAsStateWithLifecycle()
    val speechRate by model.speechRate.collectAsStateWithLifecycle()
    val smoothVoice by model.smoothVoice.collectAsStateWithLifecycle()
    val speaking by model.speaking.collectAsStateWithLifecycle()
    val urduVoiceMissing by model.urduVoiceMissing.collectAsStateWithLifecycle()
    val voiceLabel by model.voiceLabel.collectAsStateWithLifecycle()

    Scaffold(containerColor = MaterialTheme.colorScheme.background) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .imePadding()
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 20.dp, vertical = 16.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp),
        ) {
            Text(
                text = "English to Urdu",
                style = MaterialTheme.typography.headlineMedium,
                color = MaterialTheme.colorScheme.primary,
            )
            Text(
                text = "Technical words stay in English. The rest of the sentence is spoken in Urdu.",
                style = MaterialTheme.typography.bodyMedium,
            )
            OutlinedTextField(
                value = input,
                onValueChange = model::setInput,
                modifier = Modifier.fillMaxWidth(),
                label = { Text("English text") },
                placeholder = { Text("Today we will study Artificial Intelligence in Python.") },
                minLines = 5,
            )
            OutlinedTextField(
                value = keywords,
                onValueChange = model::setKeywords,
                modifier = Modifier.fillMaxWidth(),
                label = { Text("English words to keep") },
                placeholder = { Text("Artificial Intelligence, Python, TTS") },
                supportingText = { Text("Separate words with commas.") },
                minLines = 2,
            )
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Text(
                    text = "Also keep capitalized terms, acronyms, and quoted words",
                    modifier = Modifier.weight(1f).padding(end = 12.dp),
                    style = MaterialTheme.typography.bodyMedium,
                )
                Switch(checked = autoPreserve, onCheckedChange = model::setAutoPreserve)
            }
            Button(
                onClick = model::translateAndSpeak,
                enabled = !busy,
                modifier = Modifier.fillMaxWidth(),
            ) {
                Text(if (busy) "Working…" else "Translate & Speak")
            }
            if (downloading) {
                LinearProgressIndicator(modifier = Modifier.fillMaxWidth())
                Text(
                    text = "Downloading the Urdu language model…",
                    style = MaterialTheme.typography.bodySmall,
                )
            }
            Text(text = status, style = MaterialTheme.typography.bodySmall)
            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
            ) {
                Text(
                    text = result.ifBlank { "The mixed Urdu and English line will appear here." },
                    modifier = Modifier.padding(16.dp),
                    style = TextStyle(
                        fontSize = 20.sp,
                        lineHeight = 32.sp,
                        textDirection = TextDirection.Content,
                        color = MaterialTheme.colorScheme.onSurface,
                    ),
                )
            }
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Button(onClick = model::play, enabled = result.isNotBlank() && !busy) {
                    Text(if (speaking) "Play again" else "Play")
                }
                OutlinedButton(onClick = model::stop, enabled = speaking) {
                    Text("Stop")
                }
            }
            Text(
                text = "Speech rate ${String.format(Locale.US, "%.1f", speechRate)}×",
                style = MaterialTheme.typography.titleSmall,
            )
            Slider(
                value = speechRate,
                onValueChange = model::setSpeechRate,
                valueRange = 0.5f..2f,
            )
            Text(text = "Playback", style = MaterialTheme.typography.titleSmall)
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                FilterChip(
                    selected = smoothVoice,
                    onClick = { model.setSmoothVoice(true) },
                    label = { Text("Smooth ur-PK") },
                )
                FilterChip(
                    selected = !smoothVoice,
                    onClick = { model.setSmoothVoice(false) },
                    label = { Text("Dual voice") },
                )
            }
            Text(
                text = if (smoothVoice) {
                    "One Urdu voice reads the whole line, including the English words."
                } else {
                    "Urdu pieces use ur-PK. English words switch to en-US."
                },
                style = MaterialTheme.typography.bodySmall,
            )
            Text(text = voiceLabel, style = MaterialTheme.typography.bodySmall)
            if (urduVoiceMissing) {
                TextButton(onClick = model::openTtsSettings) {
                    Text("Install or choose the Urdu voice")
                }
            }
        }
    }
}
