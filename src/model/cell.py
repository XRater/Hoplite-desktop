from enum import Enum


class CellType(Enum):
    WALL = 1
    FLOOR = 2


class CellVision(Enum):
    VISIBLE = 1,
    FOGGED = 2,
    UNSEEN = 3


class Cell(object):
    def __init__(self, row, column, cell_type=CellType.WALL, is_visible=False):
        self.row = row
        self.column = column
        self.cell_type = cell_type
        self.is_visible = is_visible
        self.vision = CellVision.UNSEEN

    def __str__(self):
        return str((self.row, self.column))

    @classmethod
    def dist(cls, cell1, cell2):
        """
        Calculating a distance with cityblock metric.
        :param cell1: first cell
        :param cell2: second cell
        :return: a distance
        """
        return abs(cell1.row - cell2.row) + abs(cell1.column - cell2.column)
