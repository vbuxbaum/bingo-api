from fastapi.testclient import TestClient
import pytest
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_home(client):
    res = client.get("/")
    assert res.status_code == 200
    assert (
        "Let's play! Visit route /card for a random classic card."
        in res.json()["message"]
    )


def test_get_default_card(client):
    res = client.get("/card")
    assert res.status_code == 200
    assert res.json()["card_type"] == "classic"
    assert len(res.json()["card_values"]) == 5


def test_get_card_valid_type(client):
    res = client.get("/card?card_type=classic")
    assert res.status_code == 200
    assert res.json()["card_type"] == "classic"


def test_get_card_invalid_type(client):
    res = client.get("/card?card_type=invalid_type")
    assert res.status_code == 404
    err_msg = res.json()["detail"]
    assert err_msg == "The 'invalid_type' card type is unknown."


def test_get_card_unique_values(client):
    res = client.get("/card")
    assert res.status_code == 200
    card_values = set()
    for columns in res.json()["card_values"]:
        for value in columns:
            card_values.add(value)

    assert len(card_values) == len(res.json()["card_values"]) ** 2


def test_get_card_wild_card(client):
    res = client.get("/card")
    assert res.status_code == 200
    card_values = res.json()["card_values"]

    assert card_values[len(card_values) // 2][len(card_values) // 2] is None


def test_get_n_default_columns_card(client):
    res = client.get("/card?card_type=n_square")
    assert res.status_code == 200
    assert res.json()["card_type"] == "n_square"
    assert len(res.json()["card_values"]) == 5


def test_get_n_3_columns_card(client):
    res = client.get("/card?card_type=n_square&n=3")
    assert res.status_code == 200
    assert res.json()["card_type"] == "n_square"
    assert len(res.json()["card_values"]) == 3


def test_get_n_8_columns_card(client):
    res = client.get("/card?card_type=n_square&n=8")
    assert res.status_code == 200
    assert res.json()["card_type"] == "n_square"
    assert len(res.json()["card_values"]) == 8


def test_get_n_card_invalid_n(client):
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


def test_get_n_3_card_wild_card(client):
    res = client.get("/card?card_type=n_square&n=3")
    assert res.status_code == 200
    card_values = res.json()["card_values"]

    assert card_values[len(card_values) // 2][len(card_values) // 2] is None


def test_get_n_9_card_wild_card(client):
    res = client.get("/card?card_type=n_square&n=9")
    assert res.status_code == 200
    card_values = res.json()["card_values"]

    assert card_values[len(card_values) // 2][len(card_values) // 2] is None


def test_get_n_2_card_center_ok(client):
    res = client.get("/card?card_type=n_square&n=2")
    assert res.status_code == 200
    card_values = res.json()["card_values"]

    assert (
        type(card_values[len(card_values) // 2][len(card_values) // 2])
        is int
    )


def test_get_n_4_card_center_ok(client):
    res = client.get("/card?card_type=n_square&n=4")
    assert res.status_code == 200
    card_values = res.json()["card_values"]

    assert (
        type(card_values[len(card_values) // 2][len(card_values) // 2])
        is int
    )
