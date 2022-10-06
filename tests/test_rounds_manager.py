import mongomock
from app.services.rounds_manager import RoundManager
from tests.factories.round_factory import RoundFactory
import pytest
from hypothesis import given, HealthCheck, settings, strategies as st
from factory import Faker


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


def test_join_classic_round(isolated_round_manager):
    created_round = isolated_round_manager.create(
        RoundFactory(cards_type="classic")
    )
    joined_round = isolated_round_manager.join_with_pin(
        created_round["pin"], player_name="test player"
    )
    assert len(joined_round["joined_players"]) == 1


def test_join_inexistent_round_fails(isolated_round_manager):
    joined_round = isolated_round_manager.join_with_pin(
        "inexistent_pin", player_name="test player"
    )
    assert joined_round is None


def test_unique_cards_in_round(isolated_round_manager):
    created_round = isolated_round_manager.create(
        RoundFactory(cards_type="classic")
    )
    players_to_join = 100
    for _ in range(players_to_join):
        joined_round = isolated_round_manager.join_with_pin(
            created_round["pin"], player_name=str(Faker("name"))
        )
    assert len(joined_round["joined_players"]) == players_to_join


def test_pick_number_for_round(isolated_round_manager):
    created_round = isolated_round_manager.create(RoundFactory())
    updated_round = isolated_round_manager.pick_number(created_round["_id"])
    assert updated_round["is_round_over"] is False
    assert updated_round["most_recently_picked"] is not None
    assert len(updated_round["numbers_picked"]) == 1

    updated_round = isolated_round_manager.pick_number(created_round["_id"])
    assert len(updated_round["numbers_picked"]) == 2


def test_pick_numbers_until_round_is_over(isolated_round_manager):
    created_round = isolated_round_manager.create(RoundFactory())
    total_numbers = len(created_round["numbers_to_pick"])
    for _ in range(total_numbers):
        updated_round = isolated_round_manager.pick_number(
            created_round["_id"]
        )
    last_picked = updated_round["most_recently_picked"]
    assert last_picked is not None
    assert len(updated_round["numbers_picked"]) == total_numbers
    assert len(updated_round["numbers_to_pick"]) == 0
    assert updated_round["is_round_over"] is True

    ended_round = isolated_round_manager.pick_number(created_round["_id"])
    assert ended_round["most_recently_picked"] == last_picked
    assert len(ended_round["numbers_picked"]) == total_numbers
    assert len(ended_round["numbers_to_pick"]) == 0
    assert ended_round["is_round_over"] is True


def test_pick_number_for_inexistent_round_fails(isolated_round_manager):
    round_to_pick = isolated_round_manager.pick_number("inexistent_id")
    assert round_to_pick is None


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
