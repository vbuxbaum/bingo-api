from pymongo.collection import ReturnDocument
from fastapi.encoders import jsonable_encoder
from pymongo.results import DeleteResult

from app.models.base_model import db
from app.models.round_model import RoundModel


class RoundManager:
    db_collection = db["rounds"]

    @classmethod
    async def create(cls, round: RoundModel):
        round.numbers_to_pick = list(range(1, 76))
        round = jsonable_encoder(round)
        new_round = await cls.db_collection.insert_one(round)
        created_round = await cls.db_collection.find_one(
            {"_id": new_round.inserted_id}
        )
        del round
        return created_round

    @classmethod
    async def get_many(cls):
        return await cls.db_collection.find().to_list(1000)

    @classmethod
    async def get_one_by_id(cls, id):
        return await cls.db_collection.find_one({"_id": id})

    @classmethod
    async def get_one_by_pin(cls, pin):
        return await cls.db_collection.find_one({"pin": pin})

    @classmethod
    async def pick_number(cls, id):
        found_round = await cls.get_one_by_id(id)
        if not found_round:
            return None
        if found_round["is_round_over"]:
            return found_round

        round = RoundModel(**found_round)
        round.pick_number()

        updated_round = await cls.db_collection.find_one_and_replace(
            {"_id": id},
            jsonable_encoder(round),
            return_document=ReturnDocument.AFTER,
        )
        del round
        return updated_round

    @classmethod
    async def delete_one(cls, id: str) -> bool:
        delete_result: DeleteResult = await cls.db_collection.delete_one(
            {"_id": id}
        )
        return bool(delete_result.deleted_count)
