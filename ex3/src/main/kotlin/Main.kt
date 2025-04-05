import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.serialization.kotlinx.json.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.http.*
import kotlinx.serialization.Serializable
import io.github.cdimascio.dotenv.Dotenv

val dotenv = Dotenv.load()

@Serializable
data class Message(val content: String)

suspend fun main() {

    val webhookUrl = dotenv["WEBHOOK"] ?: "default_value"
    val message = Message("Hello from Ktor framework!")

    val client = HttpClient(CIO) {
        install(ContentNegotiation) {
            json()
        }
    }

    val response: HttpResponse = client.post(webhookUrl) {
        contentType(ContentType.Application.Json)
        setBody(message)
    }


    client.close()
}