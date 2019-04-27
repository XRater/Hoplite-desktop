import logging

from src.controller.turn_result import TurnResult
from src.model.cell import CellVision
from src.model.logic.enemy_logic import EnemyLogic
from src.model.logic.field_logic import FieldLogic
from src.model.logic.fight_logic import FightLogic
from src.model.logic.player_logic import PlayerLogic


class Logic(object):
    def __init__(self, dungeon):
        self._dungeon = dungeon
        self._init_logics()
        self._init_dungeon()

    def _init_logics(self):
        self.field_logic = FieldLogic(self, self._dungeon)
        self.player_logic = PlayerLogic(self, self._dungeon)
        self.enemy_logic = EnemyLogic(self, self._dungeon)
        self.fight_logic = FightLogic(self, self._dungeon)

    def _init_dungeon(self):
        player = self._dungeon.player
        player_room = self._dungeon.field.get_room_for_cell(player.cell)
        self.field_logic.set_vision_for_room(player_room, CellVision.VISIBLE)

    def move_player(self, delta_row, delta_column):
        """

        :param delta_row: difference for rows
        :param delta_column: difference for columns
        :return: true if player was moved and false otherwise
        """
        player = self._dungeon.player
        new_row = player.cell.row + delta_row
        new_column = player.cell.column + delta_column
        return self.player_logic.move_to_position(new_row, new_column)

    def equip_item(self, item_index):
        return self.player_logic.wear_equipment(item_index)

    def make_turn(self):
        logging.info("Making turns as enemies")
        player = self._dungeon.player
        enemies = self._dungeon.field.get_enemies()
        for enemy in enemies:
            self.enemy_logic.make_enemy_turn(enemy)
        if not player.is_alive():
            return TurnResult.GAME_OVER
        return TurnResult.TURN_ACCEPTED
