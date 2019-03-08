from .cell import Cell


class Room(object):
    def __init__(self, height, width, corner_row, corner_column):
        self.height = height
        self.width = width
        self.corner_row = corner_row
        self.corner_column = corner_column
