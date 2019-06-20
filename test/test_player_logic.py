from src.controller.turn_result import TurnResult
from src.model.cell import CellType
from src.model.logic.logic import Logic
from src.model.dungeon import Dungeon
from src.model.field import Field


def build_test_logic_player_logic_and_field():
    field = Field()
    dungeon = Dungeon(field)
    logic = Logic(dungeon)
    return logic, logic.player_logic, field


def test_player_logic_move_to_position():
    logic, player_logic, field = build_test_logic_player_logic_and_field()
    player_id = logic.add_new_player()
    player = field.find_player(player_id)
    row, col = player.cell.row, player.cell.column
    for direction in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
        new_row, new_col = row + direction[0], col + direction[1]
        assert player_logic.move_to_position(player, new_row, new_col) != TurnResult.BAD_TURN or \
               field.cells[new_row][new_col].cell_type == CellType.WALL
