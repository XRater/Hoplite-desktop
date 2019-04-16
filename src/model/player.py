from src.model.game_object import GameObject


class Player(GameObject):
    def __init__(self, cell):
        super(Player, self).__init__(cell)
        self.health = 10
        self.base_damage = 2

    def get_damage(self):
        return self.base_damage

    def is_alive(self):
        return self.health > 0