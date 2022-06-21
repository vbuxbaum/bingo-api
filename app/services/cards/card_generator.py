from abc import ABC, abstractmethod
import hashlib
import random

from pydantic import BaseModel


class CardGenerator(ABC):
    @classmethod
    @abstractmethod
    def generate_card(cls):
        """Returns a dictionary with elementary card data"""
        pass

    @classmethod
    def add_wildcard(cls, card_columns: list[list]) -> None:
        """Adds 'None' to the center value"""
        center_lenght = len(card_columns) // 2
        card_columns[center_lenght][center_lenght] = None

    @classmethod
    def get_card_hash(cls, card_type: str, card_columns: list[list]) -> str:
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
    def get_card_columns(cls) -> list[list]:
        card_columns = [
            random.sample(range(i, 15 + i), 5) for i in range(1, 75, 15)
        ]
        cls.add_wildcard(card_columns)
        return card_columns


class JKNGenerator(CardGenerator):
    @classmethod
    def generate_card(cls, card_type: str, n: int) -> dict:
        card_columns = cls.get_card_columns(n)
        return {
            "card_type": card_type,
            "card_hash": cls.get_card_hash(card_type, card_columns),
            "card_columns": card_columns,
        }

    @classmethod
    def get_card_columns(cls, column_number: int) -> list[list]:
        linearity = column_number * 3
        card_columns = [
            random.sample(range(i, linearity + i), column_number)
            for i in range(1, column_number * linearity, linearity)
        ]
        if column_number % 2 != 0:
            cls.add_wildcard(card_columns)
        return card_columns


class BingoCard(BaseModel):
    pass
