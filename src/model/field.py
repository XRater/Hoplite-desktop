from src.model.cell import Cell


class Field(object):
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rooms = []
        self.game_objects = []
        self.cells = [[Cell(row, column) for row in range(height)] for column in range(width)]
        self._generate_content()

    def _generate_content(self):
        pass
