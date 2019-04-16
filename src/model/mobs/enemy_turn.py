from enum import Enum


class EnemyTurn(Enum):
    MOVE_UP = 1
    MOVE_RIGHT = 2
    MOVE_DOWN = 3
    MOVE_LEFT = 4

    @staticmethod
    def get_turn_by_move(d_row, d_column):
        if d_row == -1:
            return EnemyTurn.MOVE_UP
        elif d_row == 1:
            return EnemyTurn.MOVE_DOWN
        elif d_column == -1:
            return EnemyTurn.MOVE_LEFT
        elif d_row == 1:
            return EnemyTurn.MOVE_RIGHT

        return None

    @staticmethod
    def get_deltas_by_turn(move):
        if move == EnemyTurn.MOVE_UP:
            return -1, 0
        elif move == EnemyTurn.MOVE_DOWN:
            return 1, 0
        elif move == EnemyTurn.MOVE_LEFT:
            return 0, -1
        elif move == EnemyTurn.MOVE_RIGHT:
            return 0, 1
        return None
