from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from app.models.round_model import RoundModel
from app.services.rounds_manager import RoundManager
from app.services.authentication import validate_token

router = APIRouter(prefix="/rounds", tags=["rounds"])


async def validation(api_token: str = Query(default="")):
    if not validate_token(api_token):
        raise HTTPException(status_code=403, detail="Invalid API token")


@router.post("/create", response_model=RoundModel)
async def create_round(round: RoundModel = Body(...), _=Depends(validation)):
    return RoundManager.create(round)


@router.get("/", response_model=List[RoundModel])
async def list_rounds():
    return RoundManager.get_many()


@router.get("/{id}", response_model=RoundModel)
async def get_round_by_id(id: str):
    round = RoundManager.get_one_by_id(id)
    if round is None:
        raise HTTPException(status_code=404, detail=f"Round {id} not found")

    return round


@router.get("/pin/{pin}", response_model=RoundModel)
async def get_round_by_pin(pin: str):
    round = RoundManager.get_one_by_pin(pin)
    if round is None:
        raise HTTPException(status_code=404, detail=f"Pin {pin} not found")

    return round


@router.put("/join/{pin}", response_model=RoundModel)
async def join_round_with_pin(
    pin: str, play_name: str = Query(example="Pl4y3r"), _=Depends(validation)
):
    round = RoundManager.join_with_pin(pin, play_name)
    if round is None:
        raise HTTPException(status_code=404, detail=f"Pin {pin} not found")

    return round


@router.put("/{id}/pick", response_model=RoundModel)
async def pick_number_for_round_id(id: str, _=Depends(validation)):
    round = RoundManager.pick_number(id)

    if round is None:
        raise HTTPException(status_code=404, detail=f"Round {id} not found")

    return round


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_round(id: str, _=Depends(validation)):
    if not RoundManager.delete_one(id):
        raise HTTPException(status_code=404, detail=f"Round {id} not found")
