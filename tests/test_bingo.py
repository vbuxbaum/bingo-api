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


def test_get_card_valid_type():
    response = client.get("/card?card_type=jk_classic")
    assert response.status_code == 200
    assert response.json()["card_type"] == "jk_classic"


def test_get_card_invalid_type():
    response = client.get("/card?card_type=invalid_type")
    assert response.status_code == 404
    err_msg = response.json()["detail"]
    assert err_msg == "The 'invalid_type' card type is unknown."


def test_get_card_unique_values():
    response = client.get("/card")
    assert response.status_code == 200
    card_values = set()
    for columns in response.json()["card_columns"]:
        for value in columns:
            card_values.add(value)

    assert len(card_values) == len(response.json()["card_columns"]) ** 2


def test_get_card_wild_card():
    response = client.get("/card")
    assert response.status_code == 200
    card_columns = response.json()["card_columns"]

    assert card_columns[len(card_columns) // 2][len(card_columns) // 2] is None
