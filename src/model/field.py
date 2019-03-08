from src.model.cell import Cell
from src.model.player import Player


class Field(object):
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rooms = []
        self.game_objects = []
        self.cells = [[Cell(row, column) for row in range(height)] for column in range(width)]
        self._generate_content()

    def findPlayer(self):
        return [player for player in self.game_objects if isinstance(player, Player)]

    def _generate_content(self):
        pass
