import logging

from src.controller.turn_result import TurnResult
from src.model.cell import CellVision
from src.model.equipment.equipment import Equipment
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
            if isinstance(game_object, Equipment):
                self.collect_loot(game_object)

    def wear_equipment(self, index):
        """
        Wears equipment and returns currently wore equipment of the same body part back to the inventory, if it exists
        If inventory doesn't contain equipment with given index raises NoEquipmentException
        :param index: index
        :return: nothing
        """
        equipment = self._player.inventory[index]
        inventory = self._player.inventory
        if index >= len(self._player.inventory) or not isinstance(equipment, Equipment):
            logging.info(f"Player tried to equip item with number {index} which they does not have")
            return TurnResult.BAD_TURN
        currently_wore = self._player.get_current_equipment_of_type(equipment.equipment_type)
        self._player.equipment[equipment.equipment_type] = equipment
        if currently_wore is None:
            logging.info(f"Player equipped item with number {index}")
            self._player.inventory = inventory[:index] + inventory[index + 1:]
        else:
            logging.info(f"Player reequipped item with number {index}. Last item was put back in inventory")
            self._player.inventory[index] = currently_wore
        return TurnResult.TURN_ACCEPTED

    def collect_loot(self, item):
        """
        Adds item to inventory if it isn't full or throws raises InventoryFullException otherwise
        :param item: loot of type GameObject
        :return: noting
        """
        if self._player.has_space_in_inventoty():
            self._player.inventory.append(item)
            return