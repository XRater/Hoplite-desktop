from threading import Barrier

import numpy as np

from src.controller.turn_result import TurnResult
from src.model.dungeon import Dungeon
from src.model.field import Field
from src.model.logic.logic import Logic


class Session(object):

    def __init__(self):
        self.id = np.random.randint(1e6)
        self.dungeon = Dungeon(Field(30, 50))
        self._logic = Logic(self.dungeon)
        self._players = []
        self.ready_barrier = Barrier(1)

    def add_new_player(self):
        player_id = len(self._players)
        self._players.append(player_id)
        return self._logic.add_new_player()

    def make_turn(self, player, turn):
        self._logic.move_player(player, 0, 1)  # TODO(drews)

        self.ready_barrier.wait()
        self._logic.make_turn()
        self.ready_barrier = Barrier(len(self._players))
        is_alive = self._logic.is_player_alive(player)
        return TurnResult.GAME_OVER if not is_alive else TurnResult.TURN_ACCEPTED
