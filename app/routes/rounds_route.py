from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from app.models.round_model import RoundModel
from app.services.rounds_manager import RoundManager
from app.services.authentication import validate_token

router = APIRouter(prefix="/rounds", tags=["rounds"])


async def validation(api_token=Query()):
    if not validate_token(api_token):
        raise HTTPException(status_code=403, detail="Invalid API token")


@router.post("/create", response_model=RoundModel)
async def create_round(round: RoundModel = Body(...), _=Depends(validation)):
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


@router.put("/{id}/pick", response_model=RoundModel)
async def pick_number_for_round_id(id: str, _=Depends(validation)):
    round = await RoundManager.pick_number(id)

    if round is None:
        raise HTTPException(status_code=404, detail=f"Round {id} not found")

    return round


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_round(id: str, _=Depends(validation)):
    if not await RoundManager.delete_one(id):
        raise HTTPException(status_code=404, detail=f"Round {id} not found")
