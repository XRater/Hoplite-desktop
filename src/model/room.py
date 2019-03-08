from .cell import Cell


class Room(object):
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.cells = [[Cell(row, column, self) for column in range(width)] for row in range(height)]
        self._doors = []  # (x, y, door)
