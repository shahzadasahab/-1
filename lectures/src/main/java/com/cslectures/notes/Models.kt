package com.cslectures.notes

data class Lecture(
    val id: String,
    val kicker: String,
    val title: String,
    val deck: String,
    val blocks: List<Block>,
)

data class Block(
    val kind: String,
    val display: String,
    val speech: String,
)
