import curses
import logging

from src.controller.equipment_command import EquipmentCommand
from src.model.equipment.equipment import Equipment


class InventoryView(object):
    """A simple view for showing and configuring user's inventory."""
    WEAR_COMMAND = 'wear'
    BACK_COMMAND = 'back'
    INSTRUCTIONS = [f'Type "{WEAR_COMMAND} <id>" to wear item with this id.',
                    f'Type "{BACK_COMMAND}" to return to game']
    INVALID_COMMAND = "Invalid command. Please try again."
    BACKPACK_LINE = "Your backpack contains"
    BACKPACK_EMPTY_LINE = "Your backpack is empty for now"
    EQUIPMENT_LINE = "Your equipment"

    def __init__(self, console, controller, dungeon):
        self.console = console
        self.controller = controller
        self.player = dungeon.player

    def draw(self):
        while True:
            self.console.clear()
            height, width = self.console.getmaxyx()

            items, to_type = self._get_strings_to_type()

            for i in range(min(len(to_type), height - 1)):
                self.console.addstr(i, 0, to_type[i])

            curses.echo()
            text = self.console.getstr(height - 1, 0, 256).decode('utf-8')

            splited = text.split(' ')
            cmd = splited[0]
            if cmd == self.WEAR_COMMAND and self._check_wear_param(splited[1:], len(items)):
                self.controller.process_user_command(EquipmentCommand(int(splited[1]) - 1))
            elif cmd == self.BACK_COMMAND:
                return

            else:
                self.console.addstr(height - 1, 0, self.INVALID_COMMAND)

            self.console.getch()

    def _get_strings_to_type(self):
        items = self.player.inventory.copy()
        logging.info(items)

        if items:
            for i, item in enumerate(items):
                items[i] = str(i + 1) + '  ' + item.description
            to_type = [self.BACKPACK_LINE] + items
        else:
            to_type = [self.BACKPACK_EMPTY_LINE]

        equipment = self.player.equipment
        for k in Equipment.EquipmentType:
            if k in equipment:
                to_type.append(equipment[k].description)
            else:
                to_type.append(str(k) + ': no')

        to_type.extend([''] + self.INSTRUCTIONS + [self.EQUIPMENT_LINE])

        return items, to_type

    @staticmethod
    def _check_wear_param(params, items_len):
        if len(params) != 1 or not params[0].isdigit():
            return False
        return 1 <= int(params[0]) <= items_len
