from fastapi import APIRouter, Body, HTTPException, status
from app.models.round_model import RoundModel
from app.services.rounds_manager import RoundManager

router = APIRouter(prefix="/rounds", tags=["rounds"])


@router.post("/create", response_model=RoundModel)
async def create_round(round: RoundModel = Body(...)):
    return await RoundManager.create(round)


@router.get("/", response_model=list[RoundModel])
async def list_rounds():
    return await RoundManager.get_many()


@router.get("/{id}", response_model=RoundModel)
async def get_round_by_id(id: str):
    round = await RoundManager.get_one_by_id(id)
    if round is None:
        raise HTTPException(status_code=404, detail=f"Round {id} not found")

    return round


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_round(id: str):
    if not await RoundManager.delete_one(id):
        raise HTTPException(status_code=404, detail=f"Round {id} not found")
