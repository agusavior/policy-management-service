package com.pms.models.dbmodel

import com.pms.models.Person
import kotlinx.serialization.*


@Serializable
data class PolicyDbModel(
    val policyId: String = java.util.UUID.randomUUID().toString(),
    var insuredPersons: List<Person>,
) {
    val totalPremium: Double get() = insuredPersons.map { it.premium }.reduce { a, b -> a + b }
}