import random


def generate_card():
    return {
        "card_type": get_card_type(),
        "card_columns": get_card_columns(),
    }


def get_card_columns():
    return [random.sample(range(1, 15), 5) for _ in range(5)]


def get_card_type():
    return "jk_classic"
