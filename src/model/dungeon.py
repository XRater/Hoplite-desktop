from src.model.field import Field


class Dungeon(object):
    def __init__(self):
        self.field = Field()
        self.player = self.field.find_player()
