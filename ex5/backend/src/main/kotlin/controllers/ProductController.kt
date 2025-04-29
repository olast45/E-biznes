package com.example.controllers

import com.example.models.Product
import io.ktor.server.response.*
import io.ktor.server.routing.*
import io.ktor.server.application.*

fun Route.productRoutes() {
    get("/products") {
        val products = listOf(
            Product("Telefon", 1200),
            Product("Laptop", 3000),
            Product("Słuchawki", 200)
        )
        call.respond(products)
    }
}
