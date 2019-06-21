from src.model.mobs.enemy.abstract_enemy import AbstractEnemy
from src.model.mobs.enemy.enemy_turn import EnemyTurn
from random import choice


class ConfusedEnemy(AbstractEnemy):
    def __init__(self, enemy, confusion_duration=5):
        self.enemy = enemy
        self.confusion_duration = confusion_duration

    def create_turn(self, field):
        self.confusion_duration -= 1
        moves = [move.value for move in EnemyTurn]
        return [choice(moves)]

    def unwrap(self):
        return self.enemy

    def is_under_confusion(self):
        return self.confusion_duration > 0
