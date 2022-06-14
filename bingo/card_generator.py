from abc import ABC, abstractmethod
import random


class CardGenerator(ABC):
    @classmethod
    @abstractmethod
    def generate_card(cls):
        pass

    @classmethod
    def add_wildcard(cls, card_columns: list[list]) -> None:
        center_lenght = len(card_columns) // 2
        card_columns[center_lenght][center_lenght] = None


class JKClassicGenerator(CardGenerator):
    @classmethod
    def generate_card(cls, card_type: str) -> dict:
        return {
            "card_type": card_type,
            "card_columns": cls.get_card_columns(),
        }

    @classmethod
    def get_card_columns(cls) -> list[list]:
        card_columns = [
            random.sample(range(i, 15 + i), 5) for i in range(1, 75, 15)
        ]
        cls.add_wildcard(card_columns)
        return card_columns
