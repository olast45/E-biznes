import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.serialization.kotlinx.json.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.http.*
import kotlinx.serialization.Serializable
import io.github.cdimascio.dotenv.Dotenv
import dev.kord.core.Kord
import dev.kord.core.event.message.MessageCreateEvent
import dev.kord.core.on
import dev.kord.gateway.Intent
import dev.kord.gateway.PrivilegedIntent

val dotenv = Dotenv.load()

@Serializable
data class Message(val content: String)

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

    val token = dotenv["TOKEN"] ?: "default_value"
    val messageContent = "Hello from Ktor framework!"
    val channelId = "1357077739412127928"
    val bot = Kord(token)


    bot.on<MessageCreateEvent> {
        if (message.author?.isBot == true) return@on
        val msg = message.content
        println("Received: $msg")

        sendMessageToChannel(token, channelId, messageContent)

    }

    bot.login {
        intents += Intent.MessageContent
    }

}