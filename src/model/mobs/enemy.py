from src.model.game_object import GameObject


class Enemy(GameObject):
    """
    Enemy 'context' class. Stores certain mob fighting strategy.
    """
    def __init__(self, cell):
        super(Enemy, self).__init__(cell)
        self.fighting_strategy = None

    def set_fighting_strategy(self, strategy):
        self.fighting_strategy = strategy

    def attack_player(self, field):
        self.fighting_strategy.attack_player(field)
