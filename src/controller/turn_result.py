from enum import Enum


class TurnResult(Enum):
    TURN_ACCEPTED = 1,
    BAD_TURN = 2,
    GAME_OVER = 3
