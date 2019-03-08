from src.model.field import Field
from src.model.player import Player


class Dungeon(object):
    def __init__(self):
        self._field = Field()
        self._player = Player()