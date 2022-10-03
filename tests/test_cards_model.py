from app.models import card_model
from app.services import card_generators


def test_compare_equal_cards():
    card_one = card_generators.ClassicGenerator.generate_card()
    card_two = card_model.BingoCard(**card_one.dict())
    assert card_one == card_two


def test_cards_hash():

    card_one = card_generators.ClassicGenerator.generate_card()
    card_two = card_model.BingoCard(**card_one.dict())
    card_three = card_generators.ClassicGenerator.generate_card()
    assert len({card_one, card_two, card_three}) == 2
