from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_home():
    res = client.get("/")
    assert res.status_code == 200
    assert (
        "Let's play! Visit /card for a random card." in res.json()["message"]
    )


def test_get_default_card():
    response = client.get("/card")
    assert response.status_code == 200
    assert response.json()["card_type"] == "jk_classic"
    assert len(response.json()["card_columns"]) == 5


def test_get_card_any_type():
    response = client.get("/card?card_type=teste")
    assert response.status_code == 200
    assert response.json()["card_type"] == "teste"


def test_get_card_unique_values():
    response = client.get("/card")
    assert response.status_code == 200
    assert response.json()["card_type"] == "jk_classic"
    card_values = set()
    for columns in response.json()["card_columns"]:
        for value in columns:
            card_values.add(value)

    assert len(card_values) == len(response.json()["card_columns"]) ** 2


def test_get_card_wild_card():
    response = client.get("/card")
    assert response.status_code == 200
    assert response.json()["card_type"] == "jk_classic"
    card_columns = response.json()["card_columns"]

    assert card_columns[len(card_columns) // 2][len(card_columns) // 2] is None
