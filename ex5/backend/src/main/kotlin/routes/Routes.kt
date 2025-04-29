package com.example.routes

import com.example.controllers.paymentRoutes
import com.example.controllers.productRoutes
import io.ktor.server.application.*
import io.ktor.server.routing.*

fun Application.configureRoutes() {
    routing {
        productRoutes()
        paymentRoutes()
    }
}
