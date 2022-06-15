from fastapi import APIRouter, Query, HTTPException

from ..services.cards.card_types import get_card_type_generator

router = APIRouter(prefix="/card", tags=['cards'])


@router.get("/")
async def get_card(
    card_type: str = Query(default="jk_classic", example="jk_classic"), 
    n: int = Query(default=5, example=5)
):
    """Provides values for a Bingo card of specified type"""

    card_generator = get_card_type_generator(card_type)
    if card_generator is None:
        raise HTTPException(
            status_code=404, detail=f"The '{card_type}' card type is unknown."
        )
    elif card_type=="jk_n" and n < 2:
        raise HTTPException(
            status_code=422, detail=f"The '{n}' number of columns is not accepted."
        )

    if card_type == "jk_classic":
        return card_generator.generate_card(card_type=card_type)
    elif card_type == "jk_n":
        return card_generator.generate_card(card_type=card_type, n=n)
