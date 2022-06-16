package com.pms.models

import kotlinx.serialization.Serializable

@Serializable
data class Person(
    val firstName: String,
    val secondName: String,
    val premium: Double,
)