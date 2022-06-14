import random


def generate_card():
    return {
        "card_type": get_card_type(),
        "card_columns": get_card_columns(),
    }


def get_card_columns():
    raw_card = [random.sample(range(i, 15 + i), 5) for i in range(1, 75, 15)]
    add_wildcard(raw_card)
    return raw_card


def add_wildcard(raw_card):
    raw_card[len(raw_card) // 2][len(raw_card) // 2] = None


def get_card_type():
    return "jk_classic"
