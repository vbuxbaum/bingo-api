import random


def generate_card(card_type="jk_classic"):
    return {
        "card_type": card_type,
        "card_columns": get_card_columns(),
    }


def get_card_columns():
    card_columns = [
        random.sample(range(i, 15 + i), 5) for i in range(1, 75, 15)
    ]
    add_wildcard(card_columns)
    return card_columns


def add_wildcard(card_columns):
    center_lenght = len(card_columns) // 2
    card_columns[center_lenght][center_lenght] = None
