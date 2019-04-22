from src.model.cell import CellType


class FieldLogic:

    def __init__(self, logic, dungeon):
        self._logic = logic
        self._dungeon = dungeon

    # Sets vision for every cell in room
    def set_vision_for_room(self, room, vision):
        for row in range(room.corner_row - 1, room.corner_row + room.height + 1):
            for column in range(room.corner_column - 1, room.corner_column + room.width + 1):
                if self.in_dungeon(row, column):
                    self._dungeon.field.cells[row][column].vision = vision

    # Sets vision for neighbour cells
    def set_vision_for_neighbour_cells(self, cell, vision):
        for delta_row, delta_col in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            new_row, new_column = cell.row + delta_row, cell.column + delta_col
            if self.in_dungeon(new_row, new_column):
                self._dungeon.field.cells[new_row][new_column].vision = vision

    # Checks if field is in dungeon
    def in_dungeon(self, row, column):
        return not (row < 0 or column < 0 or row >= self._dungeon.field.height or column >= self._dungeon.field.width)

    # Checks if player can move to th target row and column
    def can_move_to(self, row, column):
        if not self.in_dungeon(row, column):
            return False
        return self.can_move_to_cell(self._dungeon.field.cells[row][column])

    # Checks if player can move to th target row and column
    def can_move_to_cell(self, cell):
        return cell.cell_type != CellType.WALL

