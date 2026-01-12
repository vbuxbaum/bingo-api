from pydantic import BaseModel, Field
from src.models.card_model import BingoCard


class RoundPlayer(BaseModel):
    player_name: str = Field(...)
    card: BingoCard = Field(...)

    def __hash__(self):
        return hash(self.card)
