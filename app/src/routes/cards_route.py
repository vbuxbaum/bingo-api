from fastapi import APIRouter, Query, HTTPException, status

from src.models.card_model import BingoCard
from src.services.card_generators import CARD_GENERATORS

router = APIRouter(prefix="/card", tags=["cards"])

generators_examples = {
    k: {
        "value": k,
    }
    for k in CARD_GENERATORS
}


@router.get("/", response_model=BingoCard)
def get_card(
    card_type: str = Query(default="classic", examples=generators_examples),
    card_size: int = Query(default=5, example=5, ge=2, alias="n"),
):
    """Provides values for a Bingo card of specified type"""

    try:
        return CARD_GENERATORS[card_type].generate_card(n=card_size)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The '{card_type}' card type is unknown.",
        )
