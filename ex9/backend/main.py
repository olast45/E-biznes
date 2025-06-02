from fastapi import FastAPI
import requests
import os
from dotenv import load_dotenv
from conversation_phrases import get_random_greeting, get_random_farewell

load_dotenv()

app = FastAPI()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")  
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192"

from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192"

class ChatRequest(BaseModel):
    message: str

@app.get("/start-conversation")
def start_session():
    return {"message": get_random_greeting()}

@app.get("/end-conversation")
def end_session():
    return {"message": get_random_farewell()}

@app.post("/chat")
def chat(request: ChatRequest):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": request.message}]
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

