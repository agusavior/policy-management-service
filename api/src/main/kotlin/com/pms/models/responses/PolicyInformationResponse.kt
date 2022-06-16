package com.pms.models.responses

import com.pms.models.Person
import kotlinx.serialization.*

@Serializable
data class PolicyInformationResponse(
    val policyId: String,
    val requestDate: String,
    val insuredPersons: List<Person>,
    val totalPremium: Double,
)
