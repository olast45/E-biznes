import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.serialization.kotlinx.json.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.http.*
import kotlinx.serialization.Serializable
import dev.kord.core.Kord
import dev.kord.core.event.message.MessageCreateEvent
import dev.kord.core.on
import dev.kord.gateway.Intent
import dev.kord.gateway.PrivilegedIntent

@Serializable
data class Message(val content: String)

@Serializable
data class Product(val name: String, val price: Long, val category: String)

suspend fun sendMessageToChannel(botToken: String, channelId: String, messageContent: String) {
    val client = HttpClient(CIO) {
        install(ContentNegotiation) {
            json()
        }
    }

    val message = Message(content = messageContent)

    val response: HttpResponse = client.post("https://discord.com/api/v10/channels/$channelId/messages") {
        headers {
            append(HttpHeaders.Authorization, "Bot $botToken")
            append(HttpHeaders.ContentType, ContentType.Application.Json)
        }
        setBody(message)
    }

    client.close()
}

@OptIn(PrivilegedIntent::class)
suspend fun main() {

    val bot = Kord(token)

    bot.on<MessageCreateEvent> {
        if (message.author?.isBot == true) return@on
        val msg = message.content
        if (msg == "categories") {
            val categoriesToString = categories.joinToString(prefix = "Available categories:\n", separator = "\n")
            sendMessageToChannel(token, channelId, categoriesToString)
        }
        else if (categories.contains(msg)) {
            val filteredProducts = products.filter { it.category == msg }
            val productsToString = filteredProducts.joinToString(prefix = "Available products for this category:\n", separator = "\n")
            sendMessageToChannel(token, channelId, productsToString)
        }
        else {
            sendMessageToChannel(token, channelId, messageContent)
        }

    }

    bot.login {
        intents += Intent.MessageContent
    }

}