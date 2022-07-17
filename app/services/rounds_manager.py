from app.models.base_model import db
from fastapi.encoders import jsonable_encoder
from pymongo.results import DeleteResult


class RoundManager:
    rounds_collection = db["rounds"]

    @staticmethod
    async def create(round):
        round = jsonable_encoder(round)
        new_round = await db["rounds"].insert_one(round)
        created_round = await db["rounds"].find_one(
            {"_id": new_round.inserted_id}
        )
        return created_round

    @staticmethod
    async def get_many():
        return await db["rounds"].find().to_list(1000)

    @staticmethod
    async def get_one_by_id(id):
        return await db["rounds"].find_one({"_id": id})

    @staticmethod
    async def delete_one(id: str) -> bool:
        delete_result: DeleteResult = await db["rounds"].delete_one(
            {"_id": id}
        )
        return bool(delete_result.deleted_count)
