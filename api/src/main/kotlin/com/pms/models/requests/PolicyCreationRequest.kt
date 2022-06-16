package com.pms.models.requests
import com.pms.models.Person
import kotlinx.serialization.*


@Serializable
data class PolicyCreationRequest(
    val startDate: String,
    val insuredPersons: List<Person>,
)