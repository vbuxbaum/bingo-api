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
        "Let's play! Visit route /card for a random card."
        in res.json()["message"]
    )


def test_get_default_card(client):
    res = client.get("/card")
    assert res.status_code == 200
    assert res.json()["card_type"] == "jk_classic"
    assert len(res.json()["card_columns"]) == 5


def test_get_card_valid_type(client):
    res = client.get("/card?card_type=jk_classic")
    assert res.status_code == 200
    assert res.json()["card_type"] == "jk_classic"


def test_get_card_invalid_type(client):
    res = client.get("/card?card_type=invalid_type")
    assert res.status_code == 404
    err_msg = res.json()["detail"]
    assert err_msg == "The 'invalid_type' card type is unknown."


def test_get_card_unique_values(client):
    res = client.get("/card")
    assert res.status_code == 200
    card_values = set()
    for columns in res.json()["card_columns"]:
        for value in columns:
            card_values.add(value)

    assert len(card_values) == len(res.json()["card_columns"]) ** 2


def test_get_card_wild_card(client):
    res = client.get("/card")
    assert res.status_code == 200
    card_columns = res.json()["card_columns"]

    assert card_columns[len(card_columns) // 2][len(card_columns) // 2] is None
