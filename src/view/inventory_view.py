import curses

from src.controller.equipment_command import EquipmentCommand
from src.model.equipment.equipment import Equipment


class InventoryView(object):
    """A simple view for showing and configuring user's inventory."""
    WEAR_COMMAND = 'wear'
    BACK_COMMAND = 'back'
    INSTRUCTIONS = [f'Type "{WEAR_COMMAND} <id>" to wear item with this id.',
                    f'Type "{BACK_COMMAND}" to return to game']
    INVALID_COMMAND = "Invalid command. Please try again."
    EQUIPMENT_LINE = "Your equipment"

    def __init__(self, console, controller, dungeon):
        self.console = console
        self.controller = controller
        self.player = dungeon.player

    def draw(self):
        while True:
            self.console.clear()
            height, width = self.console.getmaxyx()

            items, to_type = self.get_sttrins_to_type()

            for i in range(min(len(to_type), height - 1)):
                self.console.addstr(i, 0, to_type[i])

            curses.echo()
            text = self.console.getstr(height - 1, 0, 256).decode('utf-8')

            splited = text.split(' ')
            cmd = splited[0]
            if cmd == self.WEAR_COMMAND and self.check_wear_param(splited[1:], len(items)):
                self.controller.process_user_command(EquipmentCommand(int(splited[1:])))
                # Call controller
                pass
            elif cmd == self.BACK_COMMAND:
                return

            else:
                self.console.addstr(height - 1, 0, self.INVALID_COMMAND)

            self.console.getch()

    def get_sttrins_to_type(self):
        # Get item list
        items = ["A super helmet", "Unbelievable sword"]
        for i, item in enumerate(items):
            items[i] = str(i + 1) + '  ' + item

        to_type = items + [''] + self.INSTRUCTIONS + [self.EQUIPMENT_LINE]
        equipment = self.player.equipment
        for k in Equipment.EquipmentType.__members__.keys():
            if k in equipment:
                to_type.append(equipment[k].description)
            else:
                to_type.append(str(k) + ": no")

        return items, to_type

    @staticmethod
    def check_wear_param(params, items_len):
        if len(params) != 1 or not params[0].isdigit():
            return False
        return 1 <= int(params[0]) <= items_len
