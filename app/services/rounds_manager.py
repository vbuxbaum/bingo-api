from pymongo.collection import ReturnDocument
from fastapi.encoders import jsonable_encoder
from pymongo.results import DeleteResult

from app.models.base_model import db
from app.models.round_model import RoundModel


class RoundManager:
    db_collection = db["rounds"]

    @classmethod
    def create(cls, round: RoundModel):
        round.numbers_to_pick = list(range(1, 76))
        round = jsonable_encoder(round)
        new_round = cls.db_collection.insert_one(round)
        created_round = cls.db_collection.find_one(
            {"_id": new_round.inserted_id}
        )
        del round
        return created_round

    @classmethod
    def get_many(cls):
        return list(cls.db_collection.find())

    @classmethod
    def get_one_by_id(cls, id):
        return cls.db_collection.find_one({"_id": id})

    @classmethod
    def get_one_by_pin(cls, pin):
        return cls.db_collection.find_one({"pin": pin})

    @classmethod
    def pick_number(cls, id):
        found_round = cls.get_one_by_id(id)
        if not found_round:
            return None
        if found_round["is_round_over"]:
            return found_round

        round = RoundModel(**found_round)
        round.pick_number()

        updated_round = cls.db_collection.find_one_and_replace(
            {"_id": id},
            jsonable_encoder(round),
            return_document=ReturnDocument.AFTER,
        )
        del round
        return updated_round

    @classmethod
    def delete_one(cls, id: str) -> bool:
        delete_result: DeleteResult = cls.db_collection.delete_one({"_id": id})
        return bool(delete_result.deleted_count)
