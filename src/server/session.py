import logging
from threading import Barrier

import numpy as np

from proto.generated.game_controller_pb2 import *
from src.controller.equipment_command import EquipmentCommand
from src.controller.turn_result import TurnResult
from src.model.dungeon import Dungeon
from src.model.field import Field
from src.model.logic.logic import Logic


class Session(object):
    """
    A class that stores all information about a particular session.
    """

    def __init__(self):
        self.id = np.random.randint(np.iinfo(np.intc).max)
        self.dungeon = Dungeon(Field(30, 50))
        self._logic = Logic(self.dungeon)
        self._players = []
        self.ready_barrier = Barrier(1, action=self._enemy_turn)

    def add_new_player(self):
        """
        Adding a new player in the session.
        """
        player_id = self._logic.add_new_player()
        self._players.append(player_id)
        return player_id

    def make_turn(self, player, turn):
        """
        Making player's turn. Then waiting for all other players with their turns and making mob's turn.
        :param player: a player that performed the turn.
        :param turn: turn of the player
        :return: TurnResult which is one of TURN_ACCEPTED and GAME_OVER if the player died.
        """
        if turn.equipment_operation.equipment_item != -1:
            command = EquipmentCommand(turn.equipment_operation.equipment_item,
                                       turn.equipment_operation.player_id)
            command.execute(self._logic)

        if turn.move == UP:
            self._logic.move_player(player, -1, 0)
        elif turn.move == DOWN:
            self._logic.move_player(player, 1, 0)
        elif turn.move == LEFT:
            self._logic.move_player(player, 0, -1)
        elif turn.move == RIGHT:
            self._logic.move_player(player, 0, 1)

        self.ready_barrier.wait()

        is_alive = self._logic.is_player_alive(player)
        if not is_alive:
            self._logic.remove_player(player)
            self._players.remove(player)
            self._renew_barrier()
        return TurnResult.GAME_OVER if not is_alive else TurnResult.TURN_ACCEPTED

    def _enemy_turn(self):
        self._logic.make_turn()
        self._renew_barrier()
        logging.info(f'Restored barrier in session {self.id} for {len(self._players)} players')

    def _renew_barrier(self):
        self.ready_barrier = Barrier(max(len(self._players), 1), action=self._enemy_turn)
