from pymongo.collection import ReturnDocument
from fastapi.encoders import jsonable_encoder
from pymongo.results import DeleteResult

from app.models.base_model import db
from app.models.round_model import RoundModel


class RoundManager:
    rounds_collection = db["rounds"]

    @staticmethod
    async def create(round: RoundModel):
        round.numbers_to_pick = list(range(1, 76))
        round = jsonable_encoder(round)
        new_round = await db["rounds"].insert_one(round)
        created_round = await db["rounds"].find_one(
            {"_id": new_round.inserted_id}
        )
        del round
        return created_round

    @staticmethod
    async def get_many():
        return await db["rounds"].find().to_list(1000)

    @staticmethod
    async def get_one_by_id(id):
        return await db["rounds"].find_one({"_id": id})

    @staticmethod
    async def pick_number(id):
        found_round = await RoundManager.get_one_by_id(id)
        if not found_round:
            return None
        if found_round["is_round_over"]:
            return found_round

        round = RoundModel(**found_round)
        round.pick_number()

        updated_round = await db["rounds"].find_one_and_replace(
            {"_id": id},
            jsonable_encoder(round),
            return_document=ReturnDocument.AFTER,
        )
        del round
        return updated_round

    @staticmethod
    async def delete_one(id: str) -> bool:
        delete_result: DeleteResult = await db["rounds"].delete_one(
            {"_id": id}
        )
        return bool(delete_result.deleted_count)
