from abc import ABC, abstractmethod
import random

from app.models.card_model import BingoCard


class CardGenerator(ABC):
    @classmethod
    @abstractmethod
    def generate_card(cls) -> BingoCard:
        """Returns a dictionary with elementary card data"""
        raise NotImplementedError

    @classmethod
    def _add_wildcard(cls, card_values: list[list]) -> None:
        """Adds 'None' to the center value"""
        center_lenght = len(card_values) // 2
        card_values[center_lenght][center_lenght] = None


class ClassicGenerator(CardGenerator):
    TYPE_ID = "classic"

    @classmethod
    def generate_card(cls) -> BingoCard:
        new_card = BingoCard(
            card_values=cls.gen_card_values(), card_type=cls.TYPE_ID
        )

        new_card.set_card_hash()
        return new_card

    @classmethod
    def gen_card_values(cls) -> list[list]:
        card_columns = [
            random.sample(range(i, 15 + i), 5) for i in range(1, 75, 15)
        ]
        super()._add_wildcard(card_columns)
        return card_columns


class NSquareGenerator(CardGenerator):

    TYPE_ID = "n_square"

    @classmethod
    def generate_card(cls, n: int) -> BingoCard:
        new_card = BingoCard(
            card_values=cls.gen_card_values(n), card_type=cls.TYPE_ID
        )

        new_card.set_card_hash()
        return new_card

    @classmethod
    def gen_card_values(cls, column_number: int) -> list[list]:
        linearity = column_number * 3
        card_columns = [
            random.sample(range(i, linearity + i), column_number)
            for i in range(1, column_number * linearity, linearity)
        ]
        if column_number % 2 != 0:
            cls._add_wildcard(card_columns)
        return card_columns
