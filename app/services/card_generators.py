from abc import ABC, abstractmethod
import random

from app.models.card_model import BingoCard


class CardGenerator(ABC):
    @classmethod
    @abstractmethod
    def generate_card(cls):
        """Returns a dictionary with elementary card data"""
        raise NotImplementedError

    @classmethod
    def add_wildcard(cls, card_columns: list[list]) -> None:
        """Adds 'None' to the center value"""
        center_lenght = len(card_columns) // 2
        card_columns[center_lenght][center_lenght] = None


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
        super().add_wildcard(card_columns)
        return card_columns


class NSquareGenerator(CardGenerator):

    TYPE_ID = "n_square"

    @classmethod
    def generate_card(cls, n: int) -> dict:
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
            cls.add_wildcard(card_columns)
        return card_columns


CARD_TYPES = {
    ClassicGenerator.TYPE_ID: ClassicGenerator,
    NSquareGenerator.TYPE_ID: NSquareGenerator,
}


def get_card_type_generator(type_identifier):
    """Returns the card generator class for the informed identifier"""
    return CARD_TYPES.get(type_identifier, None)
