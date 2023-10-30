import hashlib
from typing import Any, List, Union
from pydantic import BaseModel, Field

CardRow = List[Union[int, None]]
CardValues = List[CardRow]


class BingoCard(BaseModel):
    card_values: CardValues
    card_type: str
    card_hash: str = Field(default="")

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)
        __pydantic_self__.set_card_hash()

    def __hash__(self):
        return hash(self.card_hash)

    def __eq__(self, other: Any) -> bool:
        return self.card_hash == other.card_hash

    def set_card_hash(self) -> None:
        """Sets a unique hash string for the card"""
        flatten_values = []
        for col in self.card_values:
            for value in col:
                flatten_values.append(str(value))

        flatten_values.sort()

        str_data = f"{self.card_type}{''.join(flatten_values)}"
        self.card_hash = hashlib.md5(str_data.encode()).hexdigest()
