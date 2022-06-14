from bingo.card_generator import generate_card

CARD_TYPES_MAP = {"jk_classic": generate_card}


def get_card_type_generator(type_identifyer):
    return CARD_TYPES_MAP.get(type_identifyer, None)
