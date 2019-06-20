import logging

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
        players = self._dungeon.field.find_players()
        rooms = [self._dungeon.field.get_room_for_cell(player.cell) for player in players]
        for room in rooms:
            self.field_logic.set_vision_for_room(room, CellVision.VISIBLE)

    def add_new_player(self):
        player = self._dungeon.add_new_player()
        room = self._dungeon.field.get_room_for_cell(player.cell)
        self.field_logic.set_vision_for_room(room, CellVision.VISIBLE)
        return player.id

    def move_player(self, player_id, delta_row, delta_column):
        """

        :param delta_row: difference for rows
        :param delta_column: difference for columns
        :return: true if player was moved and false otherwise
        """
        player = self._dungeon.field.find_player(player_id)
        new_row = player.cell.row + delta_row
        new_column = player.cell.column + delta_column
        result = self.player_logic.move_to_position(player, new_row, new_column)
        return result

    def equip_item(self, player_id, item_index):
        player = self._dungeon.field.find_player(player_id)
        return self.player_logic.wear_equipment(player, item_index)

    def make_turn(self):
        logging.info("Making turns as enemies")
        enemies = self._dungeon.field.get_enemies()
        for enemy in enemies:
            self.enemy_logic.make_enemy_turn(enemy)

    def is_player_alive(self, player_id):
        player = self._dungeon.field.find_player(player_id)
        return player.is_alive
