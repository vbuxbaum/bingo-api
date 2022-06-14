from fastapi import FastAPI

from bingo.card_generator import generate_card

app = FastAPI()


@app.get("/")
async def home():
    """Welcome message to the API"""
    return {"message": "Let's play! Visit /card for a random card."}


@app.get("/card")
async def get_card(card_type: str = "jk_classic"):
    """Provides values for a basic Bingo card"""
    return generate_card(card_type=card_type)
