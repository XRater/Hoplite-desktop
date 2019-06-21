from src.model.cell import CellType
from src.model.logic.logic import Logic
from src.model.dungeon import Dungeon
from src.model.field import Field


def build_test_field_logic_and_field():
    field = Field()
    dungeon = Dungeon(field)
    logic = Logic(dungeon)
    return logic.field_logic, field


def test_is_dungeon():
    logic, field = build_test_field_logic_and_field()
    assert not logic.in_dungeon(-1, 0)
    assert not logic.in_dungeon(0, -1)
    assert not logic.in_dungeon(0, field.width)
    assert not logic.in_dungeon(field.height, 0)
    for row in range(field.height):
        for column in range(field.width):
            assert logic.in_dungeon(row, column)


def test_can_move():
    logic, field = build_test_field_logic_and_field()
    assert not logic.can_move_to(-1, 0)
    assert not logic.can_move_to(0, -1)
    assert not logic.can_move_to(0, field.width)
    assert not logic.can_move_to(field.height, 0)
    for row in range(field.height):
        for column in range(field.width):
            assert logic.can_move_to(row, column) or field.cells[row][column].cell_type == CellType.WALL


def test_can_move_to_cell():
    logic, field = build_test_field_logic_and_field()
    for row in range(field.height):
        for column in range(field.width):
            assert logic.can_move_to_cell(field.cells[row][column]) or \
                   field.cells[row][column].cell_type == CellType.WALL


if __name__ == '__main__':
    test_is_dungeon()