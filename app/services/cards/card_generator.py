from abc import ABC, abstractmethod
import hashlib
import random


class CardGenerator(ABC):
    @classmethod
    @abstractmethod
    def generate_card(cls):
        """Returns a dictionary with elementary card data"""
        pass

    @classmethod
    def add_wildcard(cls, card_columns: [[]]) -> None:
        """Adds 'None' to the center value"""
        center_lenght = len(card_columns) // 2
        card_columns[center_lenght][center_lenght] = None

    @classmethod
    def get_card_hash(cls, card_type: str, card_columns: [[]]) -> str:
        """Returns a unique hash string for the card"""
        flatten_columns = [str(value) for col in card_columns for value in col]
        flatten_columns.sort()

        return hashlib.md5(
            f"{card_type}{''.join(flatten_columns)}".encode()
        ).hexdigest()


class JKClassicGenerator(CardGenerator):
    @classmethod
    def generate_card(cls, card_type: str) -> dict:
        card_columns = cls.get_card_columns()
        return {
            "card_type": card_type,
            "card_hash": cls.get_card_hash(card_type, card_columns),
            "card_columns": card_columns,
        }

    @classmethod
    def get_card_columns(cls) -> [[]]:
        card_columns = [
            random.sample(range(i, 15 + i), 5) for i in range(1, 75, 15)
        ]
        cls.add_wildcard(card_columns)
        return card_columns
