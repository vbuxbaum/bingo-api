from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_get_card():
    response = client.get("/card")
    assert response.status_code == 200
    assert response.json()["card_type"] == "jk_classic"
    assert len(response.json()["card_columns"]) == 5
