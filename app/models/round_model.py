from datetime import datetime
import random
from bson import ObjectId
from pydantic import Field

from app.models.base_model import BaseModel


def pin_generator() -> str:
    return "".join(str(random.randint(0, 9)) for _ in range(6))


class RoundModel(BaseModel):
    name: str = Field(...)
    cards_type: str = Field(...)
    pin: str = Field(default_factory=pin_generator)
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {"name": "My Bingo party", "cards_type": "classic"}
        }
