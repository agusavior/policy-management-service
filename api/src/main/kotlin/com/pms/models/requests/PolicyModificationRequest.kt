package com.pms.models.requests

import com.pms.models.Person
import kotlinx.serialization.*

@Serializable
data class PolicyModificationRequest(
    val policyId: String,
    val effectiveDate: String,
    val insuredPersons: List<Person>,
)
