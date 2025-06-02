import streamlit as st
import requests
import time

st.set_page_config(page_title="Chat with LLM", layout="centered")
MODEL_NAME = "llama3-8b-8192"
API_URL = "http://localhost:8000/chat"
START_CONV_URL = "http://localhost:8000/start-conversation"
END_CONV_URL = "http://localhost:8000/end-conversation"

st.title("🤖 Chat with LLM")
st.markdown(f"**Model:** `{MODEL_NAME}`")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "greeting_shown" not in st.session_state:
    try:
        res = requests.get(START_CONV_URL)
        if res.status_code == 200:
            greeting = res.json().get("message", "Hello!")
        else:
            greeting = "Hello! (Server error)"
    except:
        greeting = "Hello! (Could not connect to server)"
    st.session_state.messages.append({"role": "assistant", "content": greeting})
    st.session_state.greeting_shown = True

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

st.markdown(
    """
    <style>
    div.stButton > button:first-child {
        position: fixed !important;
        bottom: 45px;
        right: 230px;  /* adjust this value to align closer */
        z-index: 9999;
        width: 140px;
        background-color: #f63366;
        color: white;
        border-radius: 10px;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

end_chat = st.button("End Conversation")

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

if end_chat:
    try:
        res = requests.get(END_CONV_URL)
        if res.status_code == 200:
            farewell = res.json().get("message", "Goodbye!")
        else:
            farewell = "Goodbye!"
    except:
        farewell = "Goodbye! (Could not connect to server)"

    st.chat_message("assistant").markdown(farewell)
    st.session_state.messages.append({"role": "assistant", "content": farewell})
    st.session_state.messages.clear()
    st.session_state.greeting_shown = False
