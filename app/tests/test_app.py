from fastapi.testclient import TestClient


def test_app_health(client: TestClient):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["message"] is not None
