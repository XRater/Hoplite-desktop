import logging

from src.controller.turn_result import TurnResult
from src.model.cell import CellVision
from src.model.equipment.equipment import Equipment
from src.model.experience_converter import ExperienceConverter
from src.model.mobs.enemy.enemy import Enemy


# noinspection PyMethodMayBeStatic
class PlayerLogic:

    def __init__(self, logic, dungeon):
        self._logic = logic
        self._dungeon = dungeon

    # Try to move player to position
    def move_to_position(self, player, row, column):
        if not self._logic.field_logic.in_dungeon(row, column):
            logging.info('Player could not move to position {row} {column} (out of dungeon)'.format(
                row=row,
                column=column
            ))
            return TurnResult.BAD_TURN
        target_cell = self._dungeon.field.cells[row][column]
        return self.move_to_cell(player, target_cell)

    # Move player to cell and interact with object
    def move_to_cell(self, player, cell):
        if not self._logic.field_logic.can_move_to_cell(cell):
            logging.info('Player could not move to position {row} {column} (cause of wall)'.format(
                row=cell.row,
                column=cell.column
            ))
            return TurnResult.BAD_TURN
        if not self.interact_with_cell_objects(player, cell):
            return TurnResult.TURN_ACCEPTED
        if not self._dungeon.field.has_units_on_cell(cell):
            room = self._dungeon.field.get_room_for_cell(player.cell)
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
                    self._logic.field_logic.set_vision_for_neighbour_cells(player.cell, CellVision.FOGGED)
                    self._logic.field_logic.set_vision_for_room(new_room, CellVision.VISIBLE)
            player.cell = cell
            logging.info('Player moved to position {row} {column}'.format(row=cell.row, column=cell.column))
        return TurnResult.TURN_ACCEPTED

    # Interact with objects on cell
    def interact_with_cell_objects(self, player, cell):
        objects_on_cell = self._dungeon.field.get_object_for_cell(cell)
        has_enemies_on_cell = self._dungeon.field.has_units_on_cell(cell)
        for game_object in objects_on_cell:
            if isinstance(game_object, Enemy):
                damage = player.get_damage()
                logging.info("Attacking enemy with damage {damage}".format(damage=damage))
                self._logic.fight_logic.attack_unit(player, game_object, damage)
                has_enemy = True
            if isinstance(game_object, Equipment) and not has_enemies_on_cell:
                self.collect_loot(player, game_object)
        return not has_enemies_on_cell

    def wear_equipment(self, player, index):
        """
        Wears equipment if exists and returns currently wore equipment of the same body part back to the inventory
        :param index: index
        :return: TURN_ACCEPTED if everything is correct BAD_TURN otherwise
        """
        equipment = player.inventory[index]
        inventory = player.inventory
        if index >= len(player.inventory) or not isinstance(equipment, Equipment):
            logging.info(f"Player tried to equip item with number {index} which they does not have")
            return TurnResult.BAD_TURN
        currently_wore = player.get_current_equipment_of_type(equipment.equipment_type)
        player.equipment[equipment.equipment_type] = equipment
        if currently_wore is None:
            logging.info(f"Player equipped item with number {index}")
            inventory.pop(index)
        else:
            logging.info(f"Player reequipped item with number {index}. Last item was put back in inventory")
            player.inventory[index] = currently_wore
        return TurnResult.TURN_ACCEPTED

    def collect_loot(self, player, item):
        """
        Adds item to inventory if it isn't full
        :param item: loot of type GameObject
        :return: nothing
        """
        if player.has_space_in_inventory():
            logging.info("Player picked up an item")
            player.inventory.append(item)
            self._dungeon.field.game_objects.remove(item)

    def gain_experience(self, player, experience):
        player.experience += experience
        logging.info(f"Player got {experience} exp and now has {player.experience}")
        if player.experience >= ExperienceConverter.experience_to_new_level(player.level):
            self.level_up(player)

    def level_up(self, player):
        player.experience -= ExperienceConverter.experience_to_new_level(player.level)
        player.level += 1
        logging.info(f"Player level upped and now has {player.level} level and {player.experience} experience")
        player.base_damage += 2
        player.max_health += 30
        self.heal(player)

    def heal(self, player, amount=None):
        if amount is None:
            player.health = player.max_health
        else:
            player.health = min(player.health + amount, player.max_health)
