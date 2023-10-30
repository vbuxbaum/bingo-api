from hypothesis import given
import hypothesis.strategies as st
from src.services.card_generators import CARD_GENERATORS
from fastapi.testclient import TestClient


def test_get_default_card(client: TestClient):
    res = client.get("/card")
    assert res.status_code == 200
    assert res.json()["card_type"] == "classic"
    assert len(res.json()["card_values"]) == 5


@given(st.sampled_from(list(CARD_GENERATORS)))
def test_get_card_of_valid_type(client: TestClient, card_type):
    res = client.get(f"/card?card_type={card_type}")
    assert res.status_code == 200
    assert res.json()["card_type"] == card_type


def test_get_card_invalid_type(client: TestClient):
    res = client.get("/card?card_type=invalid_type")
    assert res.status_code == 404

    err_msg = res.json()["detail"]
    assert err_msg == "The 'invalid_type' card type is unknown."


def test_get_n_default_columns_card(client: TestClient):
    res = client.get("/card?card_type=n_square")
    assert res.status_code == 200
    assert res.json()["card_type"] == "n_square"
    assert len(res.json()["card_values"]) == 5


def test_get_n_card_invalid_card_size(client: TestClient):
    res = client.get("/card?card_type=n_square&n=1")
    assert res.status_code == 422

    expected_err = [
        {
            "ctx": {"limit_value": 2},
            "loc": ["query", "n"],
            "msg": "ensure this value is greater than or equal to 2",
            "type": "value_error.number.not_ge",
        }
    ]
    err_msg = res.json()["detail"]
    assert err_msg == expected_err
