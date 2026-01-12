from fastapi.testclient import TestClient
from tests.factories import round_factory


def test_get_current_rounds(client: TestClient, mocker):
    mock_get = mocker.patch(
        "src.services.rounds_manager.RoundManager.get_many"
    )
    mock_get.return_value = [round_factory.RoundFactory()]
    client.get("/rounds")
    mock_get.assert_called()


def test_get_round_by_id(client: TestClient, mocker):
    mock_get = mocker.patch(
        "src.services.rounds_manager.RoundManager.get_one_by_id"
    )
    mock_get.return_value = round_factory.RoundFactory()
    id_str = "g41ui24kg123b"
    client.get(f"/rounds/{id_str}")
    mock_get.assert_called_with(id_str)
