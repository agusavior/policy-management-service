package com.pms.models.requests
import com.pms.models.Person
import kotlinx.serialization.*


@Serializable
data class PolicyInformationRequest(
    val policyId: String,
    val requestDate: String,
)