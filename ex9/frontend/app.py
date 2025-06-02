import streamlit as st
import requests
import time

st.set_page_config(page_title="Chat with LLM", layout="centered")
MODEL_NAME = "llama3-8b-8192"
API_URL = "http://localhost:8000/chat" 

st.title("🤖 Chat with LLM")
st.markdown(f"**Model:** `{MODEL_NAME}`")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("...thinking...")

    try:
        response = requests.post(API_URL, json={"message": user_input})
        if response.status_code == 200:
            reply = response.json()["reply"]
        else:
            reply = "❌ Error from backend"
    except Exception as e:
        reply = f"❌ Could not connect to backend\n\n{e}"

    time.sleep(1)
    placeholder.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
