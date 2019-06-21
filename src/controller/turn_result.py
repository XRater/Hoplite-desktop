from enum import Enum, auto


class TurnResult(Enum):
    TURN_ACCEPTED = auto()
    BAD_TURN = auto()
    GAME_OVER = auto()
