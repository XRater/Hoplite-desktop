from src.model.mobs.enemy.enemy_turn import EnemyTurn
from random import choice


class ConfusedStrategyDecorator:

    def __init__(self, strategy, confusion_duration=5):
        self._strategy = strategy
        self.confusion_duration = confusion_duration

    def create_turn(self, field, current_cell):
        if self.confusion_duration == 0:
            return self._strategy.create_turn(field, current_cell)
        self.confusion_duration -= 1
        moves = [move for move in EnemyTurn]
        return [choice(moves)]

    def unwrap(self):
        return self._strategy
