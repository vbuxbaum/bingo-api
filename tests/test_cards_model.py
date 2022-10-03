from app.models import card_model
from app.services import card_generators


def test_compare_equal_cards():
    card_one = card_generators.ClassicGenerator.generate_card()
    card_two = card_model.BingoCard(**card_one.dict())
    assert card_one == card_two


def test_card_is_hashable():
    card_one = card_generators.ClassicGenerator.generate_card()
    card_two = card_model.BingoCard(**card_one.dict())
    assert set([card_one, card_two])


def test_reasonable_unique_cards():
    test_size = 100
    creation_count = 0
    card_set = set()
    while len(card_set) < test_size:
        card_set.add(card_generators.ClassicGenerator.generate_card())
        creation_count += 1

    assert test_size / creation_count > 0.98
