from src.model.mobs.enemy.abstract_enemy import AbstractEnemy
from src.model.game_object import GameObject


class Enemy(AbstractEnemy, GameObject):
    """
    Enemy 'context' class. Stores certain mob fighting strategy.
    """
    def __init__(self, cell):
        super(Enemy, self).__init__(cell)
        self.fighting_strategy = None
        self.health = 20
        self.base_damage = 2
        self.drop_loot = []

    def add_drop_loot(self, item):
        self.drop_loot.append(item)

    def set_fighting_strategy(self, strategy):
        self.fighting_strategy = strategy

    def get_damage(self):
        return self.base_damage

    def is_alive(self):
        return self.health > 0

    def attack_player(self, field):
        return self.fighting_strategy.attack_player(field, self.cell)

    def __str__(self):
        return "Enemy"

