import random

cat_names = [
    "Whiskers", "Luna", "Shadow", "Mittens", "Smokey", "Gizmo", "Tigger", "Muffin",
    "Willow", "Oreo", "Peanut", "Felix", "Cleo", "Binx", "Mochi", "Poppy",
    "Marble", "Biscuit", "Sassy", "Zorro"
]

personality_traits = [
    "Playful", "Lazy", "Curious", "Affectionate", "Sneaky", "Loyal", "Independent", "Clumsy",
    "Adventurous", "Talkative", "Grumpy", "Cuddly", "Mischievous", "Shy", "Energetic",
    "Brave", "Chill", "Demanding", "Gentle", "Observant"
]

special_traits = [
    "Laser vision", "Fish whisperer", "Pillow thief", "Midnight zoomer", "Sock hunter",
    "Window watchdog", "Keyboard napper", "Tuna detector", "Shadow jumper", "Meow magician"
]

def create_random_cat():
    name = random.choice(cat_names)
    personality = random.sample(personality_traits, 3)
    special = random.choice(special_traits)
    cat_image = "https://cataas.com/cat"

    return {
        "name": name,
        "personality": personality,
        "special_trait": special,
        "image": cat_image
    }

       