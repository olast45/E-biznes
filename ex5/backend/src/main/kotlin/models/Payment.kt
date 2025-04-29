package com.example.models

import kotlinx.serialization.Serializable

@Serializable
data class Payment(
    val creditCardNumber: String,
    val expirationDate: String,
    val cvc: Int,
    val amount: Int
)
