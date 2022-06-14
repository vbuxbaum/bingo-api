from fastapi import FastAPI, Query, HTTPException

from bingo.card_types import get_card_type_generator

app = FastAPI()


@app.get("/")
async def home():
    """Welcome message to the API"""
    return {"message": "Let's play! Visit route /card for a random card."}


@app.get("/card")
async def get_card(
    card_type: str = Query(default="jk_classic", example="jk_classic")
):
    """Provides values for a Bingo card of specified type"""

    card_generator = get_card_type_generator(card_type)
    if card_generator is None:
        raise HTTPException(
            status_code=404, detail=f"The '{card_type}' card type is unknown."
        )

    return card_generator.generate_card(card_type=card_type)
