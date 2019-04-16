import logging

from src.controller.turn_result import TurnResult
from src.model.cell import CellType, CellVision
from src.model.mobs.enemy import Enemy


class Logic(object):
    def __init__(self, dungeon):
        self._dungeon = dungeon
        self._init_dungeon()

    def _init_dungeon(self):
        player = self._dungeon.player
        player_room = self._dungeon.field.get_room_for_cell(player.cell)
        self.set_vision_for_room(player_room, CellVision.VISIBLE)

    def move_player(self, delta_row, delta_column):
        """

        :param delta_row: difference for rows
        :param delta_column: difference for columns
        :return: true if player was moved and false otherwise
        """
        player = self._dungeon.player
        new_row = player.cell.row + delta_row
        new_column = player.cell.column + delta_column
        if not (self.valid_cell(new_row, new_column)):
            logging.info('Player could not move to position {row} {column} because of wall'.format(
                row=new_row,
                column=new_column
            ))
            return TurnResult.BAD_TURN

        target_cell = self._dungeon.field.cells[new_row][new_column]
        self.interact_with_cell_objects(player, target_cell)
        if self.player_can_move_to_cell(target_cell):
            room = self._dungeon.field.get_room_for_cell(player.cell)
            self.set_vision_for_neighbor_cells(player.cell, CellVision.FOGGED)
            player.cell = target_cell
            new_room = self._dungeon.field.get_room_for_cell(player.cell)
            if room is not None:
                logging.info("Player stepped out of the room {row} {column}".format(
                    row=room.corner_row,
                    column=room.corner_column
                ))
                self.set_vision_for_room(room, CellVision.FOGGED)
            if new_room is not None:
                logging.info("Player stepped into room {row} {column}".format(
                    row=new_room.corner_row,
                    column=new_room.corner_column
                ))
                self.set_vision_for_room(new_room, CellVision.VISIBLE)
            logging.info(
                'Player moved to position {row} {column}'.format(row=target_cell.row, column=target_cell.column))
            self.set_vision_for_neighbor_cells(player.cell, CellVision.VISIBLE)
        return TurnResult.TURN_ACCEPTED

    def player_can_move_to_cell(self, target_cell):
        objects_on_cell = self._dungeon.field.get_object_for_cell(target_cell)
        for game_object in objects_on_cell:
            if isinstance(game_object, Enemy):
                return False
        return True

    def interact_with_cell_objects(self, element, target_cell):
        objects_on_cell = self._dungeon.field.get_object_for_cell(target_cell)
        for game_object in objects_on_cell:
            if isinstance(game_object, Enemy):
                self.attack(element, game_object)

    def attack(self, attacker, victim):
        damage = attacker.get_damage()
        self.dealt_damage(victim, damage)
        return True

    def dealt_damage(self, victim, damage):
        if victim.health > damage:
            victim.health = victim.health - damage
        else:
            victim.health = 0
            self._dungeon.remove_game_object(victim)

    # Checks if player can move to th target row and column
    def valid_cell(self, row, column):
        return self.in_dungeon(row, column) and self._dungeon.field.cells[row][column].cell_type != CellType.WALL

    def in_dungeon(self, row, column):
        return not (row < 0 or column < 0 or row >= self._dungeon.field.height or column >= self._dungeon.field.width)

    # Sets vision for every cell in room
    def set_vision_for_room(self, room, vision):
        for row in range(room.corner_row - 1, room.corner_row + room.height + 1):
            for column in range(room.corner_column - 1, room.corner_column + room.width + 1):
                if self.in_dungeon(row, column):
                    self._dungeon.field.cells[row][column].vision = vision

    def set_vision_for_neighbor_cells(self, cell, vision):
        for delta_row, delta_col in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            if self.in_dungeon(cell.row + delta_row, cell.column + delta_col):
                self._dungeon.field.cells[cell.row + delta_row][cell.column + delta_col].vision = vision

    def make_enemy_turn(self, enemy, strategy):
        for action in strategy:
            pass

    def make_turn(self):
        player = self._dungeon.player
        enemies = self._dungeon.field.get_enemies()
        for enemy in enemies:
            strategy = enemy.attack_player()
            self.make_enemy_turn(enemy, strategy)
        if not player.is_alive():
            return TurnResult.GAME_OVER
        return TurnResult.TURN_ACCEPTED