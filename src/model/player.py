from .game_object import GameObject


class Player(GameObject):
    def __init__(self, cell):
        super().__init__(cell)