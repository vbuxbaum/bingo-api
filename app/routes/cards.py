from fastapi import APIRouter, Query, HTTPException, status

from ..services.cards.card_types import get_card_type_generator

router = APIRouter(prefix="/card", tags=["cards"])


@router.get("/")
async def get_card(
    card_type: str = Query(default="jk_classic", example="jk_classic"),
    card_size: int = Query(default=5, example=5, ge=2, alias="n"),
):
    """Provides values for a Bingo card of specified type"""

    card_generator = get_card_type_generator(card_type)
    if card_generator is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The '{card_type}' card type is unknown.",
        )

    if card_type == "jk_classic":
        return card_generator.generate_card(card_type=card_type)
    elif card_type == "jk_n":
        return card_generator.generate_card(card_type=card_type, n=card_size)
