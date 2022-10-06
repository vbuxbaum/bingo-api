from app.services.card_generators import (
    CardGenerator,
    ClassicGenerator,
    NSquareDiagGenerator,
    NSquareGenerator,
)
from app.models.card_model import BingoCard
from hypothesis import given, strategies as st
import pytest


def get_unique_card_values(card):
    result = set()
    for row in card.card_values:
        for value in row:
            result.add(value)
    return result


def test_cant_instantiate_abs_generator():
    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        CardGenerator()


def test_cant_call_abs_generator_method():
    with pytest.raises(NotImplementedError):
        CardGenerator.generate_card()


def test_create_classic_card():
    classic_card = ClassicGenerator.generate_card()
    assert isinstance(classic_card, BingoCard)
    assert len(classic_card.card_values) == 5
    assert classic_card.card_type == "classic"

    center = len(classic_card.card_values) // 2
    assert classic_card.card_values[center][center] is None
    assert len(get_unique_card_values(classic_card)) == 25


@given(st.integers(min_value=2, max_value=10))
def test_create_n_square_card(card_size):
    n_square_card = NSquareGenerator.generate_card(n=card_size)
    assert isinstance(n_square_card, BingoCard)
    assert len(n_square_card.card_values) == card_size
    assert n_square_card.card_type == "n_square"

    unique_values = get_unique_card_values(n_square_card)
    assert len(unique_values) == (card_size**2)

    center = card_size // 2
    expected_type = type(None) if card_size % 2 else int
    assert type(n_square_card.card_values[center][center]) is expected_type


@given(st.integers(min_value=2, max_value=10))
def test_create_n_square_diag_card_card(card_size):
    n_square_diag_card = NSquareDiagGenerator.generate_card(n=card_size)
    assert isinstance(n_square_diag_card, BingoCard)
    assert len(n_square_diag_card.card_values) == card_size
    assert n_square_diag_card.card_type == "n_square_diag"

    for i, _ in enumerate(n_square_diag_card.card_values):
        assert n_square_diag_card.card_values[i][i] is None

    unique_values = get_unique_card_values(n_square_diag_card)
    assert len(unique_values) == (card_size**2) - card_size + 1
