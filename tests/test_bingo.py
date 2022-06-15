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


def test_get_n_default_columns_card(client):
    res = client.get("/card?card_type=jk_n")
    assert res.status_code == 200
    assert res.json()["card_type"] == "jk_n"
    assert len(res.json()["card_columns"]) == 5


def test_get_n_3_columns_card(client):
    res = client.get("/card?card_type=jk_n&n=3")
    assert res.status_code == 200
    assert res.json()["card_type"] == "jk_n"
    assert len(res.json()["card_columns"]) == 3

def test_get_n_8_columns_card(client):
    res = client.get("/card?card_type=jk_n&n=8")
    assert res.status_code == 200
    assert res.json()["card_type"] == "jk_n"
    assert len(res.json()["card_columns"]) == 8

def test_get_n_card_invalid_n(client):
    res = client.get("/card?card_type=jk_n&n=1")
    assert res.status_code == 422
    err_msg = res.json()["detail"]
    assert err_msg == "The '1' number of columns is not accepted."

def test_get_n_3_card_wild_card(client):
    res = client.get("/card?card_type=jk_n&n=3")
    assert res.status_code == 200
    card_columns = res.json()["card_columns"]

    assert card_columns[len(card_columns) // 2][len(card_columns) // 2] is None

def test_get_n_9_card_wild_card(client):
    res = client.get("/card?card_type=jk_n&n=9")
    assert res.status_code == 200
    card_columns = res.json()["card_columns"]

    assert card_columns[len(card_columns) // 2][len(card_columns) // 2] is None

def test_get_n_2_card_center_ok(client):
    res = client.get("/card?card_type=jk_n&n=2")
    assert res.status_code == 200
    card_columns = res.json()["card_columns"]

    assert type(card_columns[len(card_columns) // 2][len(card_columns) // 2]) is int

def test_get_n_4_card_center_ok(client):
    res = client.get("/card?card_type=jk_n&n=4")
    assert res.status_code == 200
    card_columns = res.json()["card_columns"]

    assert type(card_columns[len(card_columns) // 2][len(card_columns) // 2]) is int
