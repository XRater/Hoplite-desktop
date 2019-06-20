import curses
from curses import panel

from src.controller.equipment_command import EquipmentCommand
from src.model.equipment.equipment import Equipment


class InventoryView(object):
    """A simple view for showing and configuring user's inventory."""
    BACKPACK_LINE = 'Your backpack contains'
    BACKPACK_EMPTY_LINE = 'Your backpack is empty for now'
    EQUIPMENT_LINE = 'Your equipment'

    def __init__(self, console, controller):
        self.console = console
        self.controller = controller

    def draw(self, player):
        """
        Drawing inventory of a given player.
        :param player: a player
        :return: None
        """
        self.console.clear()
        height, width = self.console.getmaxyx()

        items, to_type = self._get_strings_to_type(player)

        for i in range(min(len(to_type), height - 1)):
            self.console.addstr(i, 0, to_type[i])

        menu = Menu(items, to_type, self.console)
        selected = menu.display()
        if selected is not None:
            self.controller.process_user_command(EquipmentCommand(selected, player.id))

    def _get_strings_to_type(self, player):
        items = player.inventory

        to_type = [self.EQUIPMENT_LINE]
        equipment = player.equipment
        for k in Equipment.EquipmentType:
            if k in equipment:
                to_type.append(equipment[k].description)
            else:
                to_type.append(k.name + ': no')

        to_type.append(self.BACKPACK_LINE if items else self.BACKPACK_EMPTY_LINE)

        return list(map(lambda item: item.description, items)), to_type

    @staticmethod
    def _check_wear_param(params, items_len):
        if len(params) != 1 or not params[0].isdigit():
            return False
        return 1 <= int(params[0]) <= items_len


class Menu(object):
    """
    Class for drawing a menu. It was taken from here https://stackoverflow.com/questions/14200721/how-to-create-a-menu-and-submenus-in-python-curses
    because curses-menu library works very bad and has a lot of open issues.
    """

    def __init__(self, items, prefix, stdscreen):
        """

        :param items: items to choose from
        :param prefix: strings to type before menu
        :param stdscreen: curses screen
        """
        self.window = stdscreen.subwin(0, 0)
        self.window.keypad(1)
        self.panel = panel.new_panel(self.window)
        self.panel.hide()
        panel.update_panels()

        self.position = 0
        self.items = items
        self.prefix = prefix
        self.items.append('exit')

    def _navigate(self, n):
        self.position += n
        if self.position < 0:
            self.position = 0
        elif self.position >= len(self.items):
            self.position = len(self.items) - 1

    def display(self):
        """
        Displaying a menu.
        :return: None if exit was chosen. Otherwise index of a chosen row.
        """
        self.panel.top()
        self.panel.show()
        self.window.clear()

        while True:
            self.window.refresh()
            curses.doupdate()
            for i, line in enumerate(self.prefix):
                self.window.addstr(1 + i, 1, line)

            for index, item in enumerate(self.items):
                if index == self.position:
                    mode = curses.A_REVERSE
                else:
                    mode = curses.A_NORMAL

                msg = '%d. %s' % (index, item)
                self.window.addstr(1 + index + len(self.prefix), 1, msg, mode)

            key = self.window.getch()

            if key in [curses.KEY_ENTER, ord('\n')]:
                self.window.clear()
                self.panel.hide()
                panel.update_panels()
                curses.doupdate()
                if self.position == len(self.items) - 1:
                    return None
                else:
                    return self.position

            elif key == curses.KEY_UP:
                self._navigate(-1)

            elif key == curses.KEY_DOWN:
                self._navigate(1)
