from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.router import tfidf_router

app = FastAPI()

app.include_router(tfidf_router)
app.mount("/static", StaticFiles(directory="src/static"), name="static")