package com.pms

import io.ktor.server.engine.*
import io.ktor.server.netty.*
import com.pms.plugins.*
import io.ktor.server.plugins.contentnegotiation.*
import io.ktor.serialization.kotlinx.json.*
import io.ktor.server.application.*
import kotlinx.serialization.json.Json

fun main() {
    embeddedServer(Netty, port = 80, host = "0.0.0.0") {
        install(ContentNegotiation) {
            json(Json {
                prettyPrint = true
                isLenient = true
            })
        }
        configureHTTP()
        configureRouting()
    }.start(wait = true)
}
