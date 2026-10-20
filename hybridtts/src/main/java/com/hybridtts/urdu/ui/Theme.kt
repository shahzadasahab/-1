package com.hybridtts.urdu.ui

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val Teal = Color(0xFF0E6B66)
private val Ink = Color(0xFF1C2430)
private val Cream = Color(0xFFF7F4EE)
private val Clay = Color(0xFF9A4524)

private val Colors = lightColorScheme(
    primary = Teal,
    onPrimary = Color.White,
    secondary = Clay,
    onSecondary = Color.White,
    background = Cream,
    onBackground = Ink,
    surface = Color.White,
    onSurface = Ink,
)

@Composable
fun HybridUrduTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = Colors,
        content = content,
    )
}
