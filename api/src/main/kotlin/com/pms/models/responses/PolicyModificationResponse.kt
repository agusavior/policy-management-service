package com.pms.models.responses

import com.pms.models.Person
import kotlinx.serialization.*

@Serializable
data class PolicyModificationResponse(
    val policyId: String,
    val effectiveDate: String,
    val insuredPersons: List<Person>,
    val totalPremium: Double,
)
