import random

conversation_openers = [
    "Hi! How can I help you today?",
    "Hello! I am waiting for your messages!",
    "Hi! Im here to help you, ask me whatever you want!",
    "Hello! Can't wait to help you out!",
    "Good morning! What would you like to chat about?"
]

conversation_closers = [
    "Goodbye! Looking forward to talk to you again!",
    "Bye! I hope that I could help!",
    "Thanks for the chat! Have a nice day!",
    "It was great talking to you!",
    "In case I don't see ya, good afternoon, good evening, and good night!"
]

def get_random_greeting():
    return random.choice(conversation_openers)
def get_random_farewell():
    return random.choice(conversation_closers)