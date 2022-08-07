import motor.motor_asyncio
from pymongo.database import Database
import pydantic
from app.config import get_settings
from bson import ObjectId


client = motor.motor_asyncio.AsyncIOMotorClient(get_settings().mongodb_url)
db: Database = client.bingo


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class BaseModel(pydantic.BaseModel):
    id: PyObjectId = pydantic.Field(default_factory=PyObjectId, alias="_id")
