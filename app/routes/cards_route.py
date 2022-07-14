from fastapi import APIRouter, Query, HTTPException, status

from app.models.card_model import BingoCard
from app.services.card_generators import get_card_type_generator

router = APIRouter(prefix="/card", tags=["cards"])


@router.get("/", response_model=BingoCard)
async def get_card(
    card_type: str = Query(default="classic", example="classic"),
    card_size: int = Query(default=5, example=5, ge=2, alias="n"),
):
    """Provides values for a Bingo card of specified type"""

    card_generator = get_card_type_generator(card_type)
    if card_generator is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The '{card_type}' card type is unknown.",
        )

    if card_type == "classic":
        return card_generator.generate_card()
    if card_type == "n_square":
        return card_generator.generate_card(n=card_size)
