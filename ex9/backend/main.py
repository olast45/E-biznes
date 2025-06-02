from fastapi import FastAPI
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")  
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192"

@app.get("/chat")
def send_test_message():
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": "Hi! How are you?"}
        ]
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return {
            "reply": response.json()["choices"][0]["message"]["content"]
        }
    else:
        return {
            "error": response.text
        }
