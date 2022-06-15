from .card_generator import JKClassicGenerator

CARD_TYPES_MAP = {"jk_classic": JKClassicGenerator}


def get_card_type_generator(type_identifier):
    '''Returns the card generator class for the informed identifier'''
    return CARD_TYPES_MAP.get(type_identifier, None)
