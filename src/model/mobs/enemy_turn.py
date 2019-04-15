from enum import Enum


class EnemyTurn(Enum):
    MOVE_UP = 1
    MOVE_RIGHT = 2
    MOVE_DOWN = 3
    MOVE_LEFT = 4
    STAY = 5
    ATTACK = 6
