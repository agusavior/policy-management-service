package com.pms.plugins


import com.pms.models.dbmodel.PolicyDbModel
import com.pms.models.requests.PolicyCreationRequest
import com.pms.models.requests.PolicyInformationRequest
import com.pms.models.requests.PolicyModificationRequest
import com.pms.models.responses.PolicyCreationResponse
import com.pms.models.responses.PolicyInformationResponse
import com.pms.models.responses.PolicyModificationResponse
import io.ktor.http.*
import io.ktor.server.routing.*
import io.ktor.server.application.*
import io.ktor.server.response.*
import io.ktor.server.request.*


fun Application.configureRouting() {
    // Create an in-memory mocked database and put elements in it
    val policyStorage = mutableListOf<PolicyDbModel>()

    // Define policy routing
    routing {
        this.route("/policy") {
            post("/creation") {
                call.receive<PolicyCreationRequest>().let { req ->
                    // Create db model
                    val policyDbModel = PolicyDbModel(
                        insuredPersons = req.insuredPersons
                    )

                    // Add to db
                    policyStorage.add(policyDbModel)

                    // Create response
                    val res = PolicyCreationResponse(
                        policyId = policyDbModel.policyId,
                        startDate = req.startDate,
                        insuredPersons = policyDbModel.insuredPersons,
                        totalPremium = policyDbModel.totalPremium,
                    )

                    // Respond
                    call.respond(res)
                }
            }
            post("/modification") {
                call.receive<PolicyModificationRequest>().let { req ->
                    // Get db model
                    val policyDbModel = policyStorage.find {
                        it.policyId == req.policyId
                    }

                    // If it does not exist, return 404 code
                    policyDbModel ?: return@let call.respond(HttpStatusCode.NotFound)

                    // Modify it
                    policyDbModel.insuredPersons = req.insuredPersons

                    // Create response
                    val res = PolicyModificationResponse(
                        policyId = policyDbModel.policyId,
                        effectiveDate = req.effectiveDate,
                        insuredPersons = policyDbModel.insuredPersons,
                        totalPremium = policyDbModel.totalPremium,
                    )

                    // Respond
                    call.respond(res)
                }
            }
            post("information") {
                call.receive<PolicyInformationRequest>().let { req ->
                    // Get db model
                    val policyDbModel = policyStorage.find {
                        it.policyId == req.policyId
                    }

                    // If it does not exist, return 404 code
                    policyDbModel ?: return@let call.respond(HttpStatusCode.NotFound)

                    // Create response
                    val res = PolicyInformationResponse(
                        policyId = policyDbModel.policyId,
                        requestDate = req.requestDate,
                        insuredPersons = policyDbModel.insuredPersons,
                        totalPremium = policyDbModel.totalPremium,
                    )

                    // Respond
                    call.respond(res)
                }
            }
        }
    }

    // Define index routing
    routing {
        get("/") {
            call.respondText("Policy management service API is running.")
        }
    }
}
