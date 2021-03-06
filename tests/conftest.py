import pytest
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def client():
    return TestClient(app)
