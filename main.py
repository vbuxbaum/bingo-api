from fastapi import FastAPI, Query, HTTPException

from bingo.card_types import get_card_type_generator

app = FastAPI()


@app.get("/")
async def home():
    """Welcome message to the API"""
    return {"message": "Let's play! Visit /card for a random card."}


@app.get("/card")
async def get_card(card_type: str = Query(default="jk_classic")):
    """Provides values for a basic Bingo card"""
    try:
        card_generator = get_card_type_generator(card_type)
    except KeyError:
        raise HTTPException(
            status_code=404, detail=f"The '{card_type}' card type is unknown."
        )

    return card_generator(card_type=card_type)
