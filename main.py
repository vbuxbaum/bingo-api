from fastapi import FastAPI

from bingo.card_generator import generate_card

app = FastAPI()


@app.get("/")
async def home():
    return {"message": "Hello World"}


@app.get("/card")
async def get_card():
    return generate_card()
