from abc import ABC, abstractmethod
import random
from typing import Type
from frozendict import frozendict

from src.models.card_model import BingoCard, CardValues


class CardGenerator(ABC):
    @classmethod
    @abstractmethod
    def generate_card(cls, **_) -> BingoCard:
        """Returns the card data based on the concrete generator"""
        raise NotImplementedError

    @classmethod
    def _add_wildcard(cls, card_values: CardValues) -> None:
        """Adds 'None' to the center value"""
        center_lenght = len(card_values) // 2
        card_values[center_lenght][center_lenght] = None


class ClassicGenerator(CardGenerator):
    TYPE_ID = "classic"

    @classmethod
    def generate_card(cls, **_) -> BingoCard:
        new_card = BingoCard(
            card_values=cls.gen_card_values(), card_type=cls.TYPE_ID
        )
        return new_card

    @classmethod
    def gen_card_values(cls) -> CardValues:
        card_columns = [
            random.sample(range(i, 15 + i), 5) for i in range(1, 75, 15)
        ]
        super()._add_wildcard(card_columns)
        return card_columns


class NSquareGenerator(CardGenerator):

    TYPE_ID = "n_square"

    @classmethod
    def generate_card(cls, **kwargs) -> BingoCard:

        new_card = BingoCard(
            card_values=cls.gen_card_values(kwargs.get("n", 5)),
            card_type=cls.TYPE_ID,
        )

        return new_card

    @classmethod
    def gen_card_values(cls, card_size: int) -> CardValues:
        linearity = card_size * 3
        card_columns = [
            random.sample(range(i, linearity + i), card_size)
            for i in range(1, card_size * linearity, linearity)
        ]
        if card_size % 2 != 0:
            cls._add_wildcard(card_columns)
        return card_columns


class NSquareDiagGenerator(NSquareGenerator):
    TYPE_ID = "n_square_diag"

    @classmethod
    def gen_card_values(cls, card_size: int) -> CardValues:
        card_columns = super().gen_card_values(card_size)

        for i in range(len(card_columns)):
            card_columns[i][i] = None

        return card_columns


CARD_GENERATORS: frozendict[str, Type[CardGenerator]] = frozendict(
    {
        ClassicGenerator.TYPE_ID: ClassicGenerator,
        NSquareGenerator.TYPE_ID: NSquareGenerator,
        NSquareDiagGenerator.TYPE_ID: NSquareDiagGenerator,
    }
)
