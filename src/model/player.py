from src.model.game_object import GameObject


class Player(GameObject):
    def __init__(self, cell):
        super(Player, self).__init__(cell)
