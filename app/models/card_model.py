import hashlib
from pydantic import BaseModel, Field


class BingoCard(BaseModel):
    card_values: list[list]
    card_type: str
    card_hash: str = Field(default='')

    def set_card_hash(self) -> None:
        """Sets a unique hash string for the card"""
        flatten_values = []
        for col in self.card_values:
            for value in col:
                flatten_values.append(str(value))

        flatten_values.sort()

        str_data = f"{self.card_type}{''.join(flatten_values)}"
        self.card_hash = hashlib.md5(str_data.encode()).hexdigest()
