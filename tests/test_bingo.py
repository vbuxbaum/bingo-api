from fastapi.testclient import TestClient
import pytest
from app.main import app

from hypothesis import given
import hypothesis.strategies as st


@pytest.fixture(scope="session")
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


@given(n=st.integers(min_value=2, max_value=20))
def test_get_n_3_columns_card(client, n):
    res = client.get(f"/card?card_type=n_square&n={n}")
    assert res.status_code == 200
    assert res.json()["card_type"] == "n_square"
    assert len(res.json()["card_values"]) == n


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


@given(n=st.integers(min_value=1, max_value=10))
def test_get_odd_saquare_card_wildcard(client, n):
    given_odd_int = n * 2 + 1
    res = client.get(f"/card?card_type=n_square&n={given_odd_int}")
    assert res.status_code == 200
    card_values = res.json()["card_values"]

    assert card_values[len(card_values) // 2][len(card_values) // 2] is None


@given(n=st.integers(min_value=1, max_value=10))
def test_get_even_saquare_card_wildcard(client, n):
    given_even_int = n * 2
    res = client.get(f"/card?card_type=n_square&n={given_even_int}")
    assert res.status_code == 200
    card_values = res.json()["card_values"]

    assert (
        type(card_values[len(card_values) // 2][len(card_values) // 2]) is int
    )


@given(n=st.integers(min_value=2, max_value=20))
def test_get_n_square_diag(client, n):
    res = client.get(f"/card?card_type=n_square_diag&n={n}")
    assert res.status_code == 200
    card_values = res.json()["card_values"]

    for i in range(len(card_values)):
        assert card_values[i][i] is None
