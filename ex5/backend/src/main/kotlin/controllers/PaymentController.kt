package com.example.controllers

import com.example.models.Payment
import io.ktor.server.request.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import io.ktor.server.application.*

fun Route.paymentRoutes() {
    post("/payment") {
        val payment = call.receive<Payment>()
        println("Received payment: $payment")
        call.respond(mapOf("status" to "OK"))
    }
}
