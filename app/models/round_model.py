from datetime import datetime
import random
from typing import List, Union
from bson.objectid import ObjectId
from pydantic import Field

from app.models.base_model import BaseModel


def pin_generator() -> str:
    return "".join(str(random.randint(0, 9)) for _ in range(6))


class RoundModel(BaseModel):
    name: str = Field(...)
    cards_type: str = Field(...)
    pin: str = Field(default_factory=pin_generator)
    most_recently_picked: Union[int, None] = Field(default=None)
    is_round_over: bool = Field(default=False)
    numbers_picked: List[int] = Field(default=[])
    numbers_to_pick: List[int] = Field(default=[])
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {"name": "My Bingo party", "cards_type": "classic"}
        }

    def pick_number(self) -> None:
        try:
            self.most_recently_picked = random.choice(self.numbers_to_pick)
        except IndexError:
            self.is_round_over = True
            return

        self.numbers_to_pick.remove(self.most_recently_picked)
        self.numbers_picked.append(self.most_recently_picked)
