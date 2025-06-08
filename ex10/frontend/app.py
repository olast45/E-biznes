import streamlit as st
import requests
import base64
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="🐾 Cat Gallery 🐱", page_icon="🐱", layout="centered")

st.markdown(
    """
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="font-family: 'Comic Sans MS', cursive, sans-serif; font-size: 3rem; margin-bottom: 0;">🐾 Cat Gallery 🐱</h1>
        <p style="font-size: 1.25rem; color: #555; margin-top: 5px;">
            Discover your purrfect feline friend and hear their meow!
        </p>
    </div>
    <hr style="border: 1px solid #eee;">
    """,
    unsafe_allow_html=True,
)

def fetch_random_cat():
    try:
        resp = requests.get(f"{API_URL}/random-cat")
        resp.raise_for_status()
        return resp.json()
    except:
        st.error("Failed to fetch a cat :(")
        return None

def fetch_meow_sound():
    try:
        resp = requests.get(f"{API_URL}/meow-sound")
        resp.raise_for_status()
        return resp.content
    except:
        st.error("Failed to play meow sound!")
        return None

def play_audio_auto(audio_bytes):
    b64 = base64.b64encode(audio_bytes).decode()
    md = f"""
    <audio autoplay controls style="width: 100%; margin-top: 15px;">
        <source src="data:audio/mpeg;base64,{b64}" type="audio/mpeg">
        Your browser does not support the audio element.
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)

if "cat_data" not in st.session_state:
    st.session_state.cat_data = fetch_random_cat()

if "meow_audio" not in st.session_state:
    st.session_state.meow_audio = None

cat_data = st.session_state.cat_data

if cat_data:

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(cat_data["image"], use_container_width=True)

    with col2:
        st.markdown(
            f"""
            <h2 style="margin-bottom: 5px;">😺 {cat_data['name']}</h2>
            <p style="font-weight: 600; margin: 5px 0;">
                <span style="color: #f39c12;">Personality traits:</span> {', '.join(cat_data['personality'])}
            </p>
            <p style="font-weight: 600; margin: 5px 0;">
                <span style="color: #e67e22;">Special trait:</span> {cat_data['special_trait']}
            </p>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True) 

st.markdown("---")

if st.button("▶️ Meow!"):
    audio = fetch_meow_sound()
    if audio:
        st.session_state.meow_audio = audio

if st.session_state.meow_audio:
    play_audio_auto(st.session_state.meow_audio)

st.markdown("---")

st.markdown(
    """
    <style>
    div.stButton > button {
        display: block;
        margin-left: auto;
        margin-right: auto;
        font-size: 20px;
        padding: 12px 40px;
        cursor: pointer;
        border-radius: 25px;
        background: #ff6f61;
        color: white;
        border: none;
        transition: background 0.3s ease, box-shadow 0.3s ease;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(255,111,97,0.4);
        margin-bottom: 10px;
    }
    div.stButton > button:hover {
        background: #ff6f61;
        color: white;
        box-shadow: 0 6px 16px rgba(255,75,62,0.6);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <p style='text-align: center; color: #888; font-size: 0.9rem;'>
        Made with ❤️ and 🐾 for all cat lovers
    </p>
    """,
    unsafe_allow_html=True,
)
