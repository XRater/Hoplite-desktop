import curses


class InventoryView(object):
    """A simple view for showing and configuring user's inventory."""
    WEAR_COMMAND = 'wear'
    BACK_COMMAND = 'back'
    INSTRUCTIONS = [f'Type "{WEAR_COMMAND} <id>" to wear item with this id.',
                    f'Type "{BACK_COMMAND}" to return to game']
    INVALID_COMMAND = "Invalid command. Please try again."

    def __init__(self, console, controller):
        self.console = console
        self.controller = controller

    def draw(self):
        while True:
            self.console.clear()
            height, width = self.console.getmaxyx()

            # Get item list
            items = ["A super helmet", "Unbelievable sword"]
            for i, item in enumerate(items):
                items[i] = str(i + 1) + '  ' + item
            to_type = items + [''] + self.INSTRUCTIONS

            for i in range(min(len(to_type), height - 1)):
                self.console.addstr(i, 0, to_type[i])

            curses.echo()
            text = self.console.getstr(height - 1, 0, 256).decode('utf-8')

            splited = text.split(' ')
            cmd = splited[0]
            if cmd == self.WEAR_COMMAND and self.check_wear_param(splited[1:], len(items)):
                # Call controller
                pass
            elif cmd == self.BACK_COMMAND:
                return

            else:
                self.console.addstr(height - 1, 0, self.INVALID_COMMAND)

            self.console.getch()

    @staticmethod
    def check_wear_param(params, items_len):
        if len(params) != 1 or not params[0].isdigit():
            return False
        return 1 <= int(params[0]) <= items_len
