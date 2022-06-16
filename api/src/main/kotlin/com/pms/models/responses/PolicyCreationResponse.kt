package com.pms.models.responses

import com.pms.models.Person
import kotlinx.serialization.*

@Serializable
data class PolicyCreationResponse(
    val policyId: String,
    val startDate: String,
    val insuredPersons: List<Person>,
    val totalPremium: Double,
)
