from src.controller.turn_result import TurnResult
from src.model.logic.logic import Logic
from src.model.dungeon import Dungeon
from src.model.field import Field


def build_test_logic_and_field():
    field = Field()
    dungeon = Dungeon(field)
    return Logic(dungeon), field


def test_logic_add_player():
    logic = build_test_logic_and_field()[0]
    player_ids = set()
    for _ in range(10):
        player_id = logic.add_new_player()
        assert player_id not in player_ids
        player_ids.add(player_id)


def test_logic_cannot_move_infinitely():
    logic, field = build_test_logic_and_field()
    player_id = logic.add_new_player()
    for direction, limit in zip([(0, 1), (0, -1), (1, 0), (-1, 0)],
                                [field.width, field.width, field.height, field.height]):
        stopped = False
        for _ in range(limit):
            stopped = stopped or logic.move_player(player_id, *direction) == TurnResult.BAD_TURN
        assert stopped


def test_logic_is_initially_alive():
    logic = build_test_logic_and_field()[0]
    player_id = logic.add_new_player()
    assert logic.is_player_alive(player_id)


def test_players_amount():
    logic, field = build_test_logic_and_field()
    last_id = 0
    for i in range(10):
        assert len(field.find_players()) == i
        last_id = logic.add_new_player()
    assert len(field.find_players()) == 10
    field.remove_player(last_id)
    assert len(field.find_players()) == 9
