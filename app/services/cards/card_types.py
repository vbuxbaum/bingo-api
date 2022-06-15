from .card_generator import JKClassicGenerator, JKNGenerator

CARD_TYPES_MAP = {"jk_classic": JKClassicGenerator, "jk_n" : JKNGenerator}


def get_card_type_generator(type_identifier):
    '''Returns the card generator class for the informed identifier'''
    return CARD_TYPES_MAP.get(type_identifier, None)
