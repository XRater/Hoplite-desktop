from enum import Enum


class CellType(Enum):
    WALL = 1
    FLOOR = 2


class Cell(object):
    def __init__(self, row, column, cell_type, is_visible):
        self.row = row
        self.column = column
        self.cell_type = cell_type
        self.is_visible = is_visible
