import random


def generate_card():
    return {
        "card_type": get_card_type(),
        "card_columns": get_card_columns(),
    }


def get_card_columns():
    return [random.sample(range(i, 15 + i), 5) for i in range(1, 75, 15)]


def get_card_type():
    return "jk_classic"
