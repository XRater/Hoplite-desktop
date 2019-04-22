import logging

from src.controller.turn_result import TurnResult
from src.model.cell import CellVision
from src.model.mobs.enemy.enemy import Enemy


class PlayerLogic:

    def __init__(self, logic, dungeon):
        self._logic = logic
        self._dungeon = dungeon
        self._player = self._dungeon.player

    # Try to move player to position
    def move_to_position(self, row, column):
        if not self._logic.field_logic.in_dungeon(row, column):
            logging.info('Player could not move to position {row} {column} (out of dungeon)'.format(
                row=row,
                column=column
            ))
            return TurnResult.BAD_TURN
        target_cell = self._dungeon.field.cells[row][column]
        return self.move_to_cell(target_cell)

    # Move player to cell and interact with object
    def move_to_cell(self, cell):
        if not self._logic.field_logic.can_move_to_cell(cell):
            logging.info('Player could not move to position {row} {column} (cause of wall)'.format(
                row=cell.row,
                column=cell.column
            ))
            return TurnResult.BAD_TURN
        self.interact_with_cell_objects(cell)
        if not self._dungeon.field.has_units_on_cell(cell):
            room = self._dungeon.field.get_room_for_cell(self._player.cell)
            new_room = self._dungeon.field.get_room_for_cell(cell)
            if room != new_room:
                pass
                if room is not None:
                    logging.info("Player stepped out of the room {row} {column}".format(
                        row=room.corner_row,
                        column=room.corner_column
                    ))
                    self._logic.field_logic.set_vision_for_room(room, CellVision.FOGGED)
                    self._logic.field_logic.set_vision_for_neighbour_cells(cell, CellVision.VISIBLE)
                if new_room is not None:
                    logging.info("Player stepped into room {row} {column}".format(
                        row=new_room.corner_row,
                        column=new_room.corner_column
                    ))
                    self._logic.field_logic.set_vision_for_neighbour_cells(self._player.cell, CellVision.FOGGED)
                    self._logic.field_logic.set_vision_for_room(new_room, CellVision.VISIBLE)
            self._player.cell = cell
            logging.info('Player moved to position {row} {column}'.format(row=cell.row, column=cell.column))
        return TurnResult.TURN_ACCEPTED

    # Interact with objects on cell
    def interact_with_cell_objects(self, cell):
        objects_on_cell = self._dungeon.field.get_object_for_cell(cell)
        for game_object in objects_on_cell:
            if isinstance(game_object, Enemy):
                damage = self._player.get_damage()
                logging.info("Attacking enemy with damage {damage}".format(damage=damage))
                self._logic.fight_logic.attack_unit(game_object, damage)
