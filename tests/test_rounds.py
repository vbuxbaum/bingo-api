import mongomock
from app.services.rounds_manager import RoundManager
from tests.factories.round_factory import RoundFactory
import pytest
from hypothesis import given, HealthCheck, settings, strategies as st


@pytest.fixture
def isolated_round_manager():
    RoundManager.db_collection = mongomock.MongoClient()["test"]["rounds"]
    return RoundManager


@given(st.builds(RoundFactory))
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_create_round(isolated_round_manager, round):
    created_round = isolated_round_manager.create(round)
    assert created_round["is_round_over"] is False
    assert created_round["most_recently_picked"] is None
    assert created_round["numbers_picked"] == []
    assert created_round["joined_players"] == []
    assert created_round["pin"].isdigit()
    assert len(created_round["pin"]) == 6


def test_create_multiple_rounds(isolated_round_manager):
    isolated_round_manager.create(RoundFactory())
    isolated_round_manager.create(RoundFactory())
    isolated_round_manager.create(RoundFactory())
    isolated_round_manager.create(RoundFactory())
    assert len(isolated_round_manager.get_many()) == 4


def test_search_by_pin(isolated_round_manager):
    created_round = isolated_round_manager.create(RoundFactory())
    found_round = isolated_round_manager.get_one_by_pin(created_round["pin"])
    assert found_round["_id"] == created_round["_id"]


def test_search_by_id(isolated_round_manager):
    created_round = isolated_round_manager.create(RoundFactory())
    found_round = isolated_round_manager.get_one_by_id(created_round["_id"])
    assert found_round["_id"] == created_round["_id"]


def test_join_round(isolated_round_manager):
    created_round = isolated_round_manager.create(RoundFactory())
    assert created_round["joined_players"] == []

    joined_round = isolated_round_manager.join_with_pin(
        created_round["pin"], player="test player"
    )
    assert len(joined_round["joined_players"])


def test_pick_number_for_round(isolated_round_manager):
    created_round = isolated_round_manager.create(RoundFactory())
    updated_round = isolated_round_manager.pick_number(created_round["_id"])
    assert updated_round["is_round_over"] is False
    assert updated_round["most_recently_picked"] is not None
    assert len(updated_round["numbers_picked"]) == 1

    updated_round = isolated_round_manager.pick_number(created_round["_id"])
    assert len(updated_round["numbers_picked"]) == 2


def test_delete_by_id(isolated_round_manager):
    created_round = isolated_round_manager.create(RoundFactory())
    assert isolated_round_manager.delete_one(created_round["_id"])
    assert len(isolated_round_manager.get_many()) == 0


def test_delete_inexistent(isolated_round_manager):
    created_round = isolated_round_manager.create(RoundFactory())
    _ = isolated_round_manager.create(RoundFactory())
    assert isolated_round_manager.delete_one(created_round["_id"])
    assert not isolated_round_manager.delete_one(created_round["_id"])
    assert len(isolated_round_manager.get_many()) == 1
