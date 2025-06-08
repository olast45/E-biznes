from fastapi import FastAPI
from cat_traits_generator import create_random_cat
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://frontend-ex10.onrender.com"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/random-cat")
def get_random_cat_traits():
    return create_random_cat()

@app.get("/meow-sound")
def get_meow_sound():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "sounds", "cat-meow.mp3")
    return FileResponse(file_path, media_type="audio/mp3")