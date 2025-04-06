import io.github.cdimascio.dotenv.Dotenv

val dotenv = Dotenv.load()

val token = dotenv["TOKEN"] ?: "default_value"

const val messageContent = "Hello from Ktor framework!"
const val channelId = "1357077739412127928"
val categories = listOf("books", "music", "fashion", "technology")
val products = listOf(
    Product("Shantaram", 30, "books"),
    Product("Iphone", 3000, "technology"),
    Product("Denim jacket", 150, "fashion"),
    Product("Leather skirt", 300, "fashion"),
    Product("Master and Margarita", 35, "books"),
    Product("FKA twigs - MAGDALENE", 50, "music"),
    Product("Lady Gaga - MAYHEM",50, "music"),
    Product("To kill a mockingbird", 40, "books")
)