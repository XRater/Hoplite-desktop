import curses

from src.model.cell import CellType, CellVision
from src.model.door import Door


class View(object):
    QUIT_BUTTON = 'q'
    WELCOME_STRING = 'Hi there! Check out our best game!\n'
    INSTRUCTION_STRING = 'Press SPACE to start game.\n'
    SAVING_SCREEN = "Please enter file where you want to save this game and press ENTER.\n" \
                    "Empty line if yoy don't want to save.\n"
    WALL_SYMBOL = '#'
    FLOOR_SYMBOL = '.'
    FOG_SYMBOL = '~'
    DOOR_SYMBOL = 'O'
    PLAYER_SYMBOL = '@'

    _red_color = 1

    def __init__(self, controller, dungeon):
        self.controller = controller
        self.dungeon = dungeon
        self.model = dungeon.field

    def start(self):
        curses.wrapper(self._draw_menu)

    def _start_game(self, console):
        command = 0

        while command != ord(self.QUIT_BUTTON):
            console.clear()
            self.height, self.width = console.getmaxyx()

            if command == curses.KEY_RIGHT:
                self.controller.pressed_right()
            if command == curses.KEY_LEFT:
                self.controller.pressed_left()
            if command == curses.KEY_UP:
                self.controller.pressed_up()
            if command == curses.KEY_DOWN:
                self.controller.pressed_down()

            self._draw_game(console)

            self._print_footer(console)
            console.refresh()
            command = console.getch()

    def _print_footer(self, console):
        footer = "Press {} to exit".format(self.QUIT_BUTTON)
        console.addstr(self.height - 1, 0, footer)
        console.addstr(self.height - 1, len(footer), " " * (self.width - len(footer) - 1))

    def _draw_menu(self, console):
        command = 0

        console.clear()
        console.refresh()

        curses.start_color()
        curses.init_pair(self._red_color, curses.COLOR_RED, curses.COLOR_BLACK)

        while command != ord(self.QUIT_BUTTON):
            console.clear()
            self.height, self.width = console.getmaxyx()

            if command == ord(' '):
                self._start_game(console)
                break

            start_x_title = self.width // 2 - len(self.WELCOME_STRING) // 2 - len(self.WELCOME_STRING) % 2
            start_x_subtitle = self.width // 2 - len(self.INSTRUCTION_STRING) // 2 - len(self.INSTRUCTION_STRING) % 2
            start_y = self.height // 2 - 2

            self._print_with_read_color(console, start_y, start_x_title, self.WELCOME_STRING)
            self._print_with_read_color(console, start_y + 1, start_x_subtitle, self.INSTRUCTION_STRING)

            self._print_footer(console)

            console.refresh()
            command = console.getch()

        self._process_exit(console)

    def _process_exit(self, console):
        console.clear()
        curses.echo()
        console.addstr(0, 0, self.SAVING_SCREEN)
        filename = console.getstr(2, 0, 256).decode('utf-8')
        if filename.strip():
            self.controller.save_field(filename)

    def _print_with_read_color(self, console, y, x, text):
        console.attron(curses.color_pair(self._red_color))
        console.attron(curses.A_BOLD)
        console.addstr(y, x, text)
        console.attroff(curses.color_pair(self._red_color))
        console.attroff(curses.A_BOLD)

    def _draw_game(self, console):
        # logging.info("Drawing field")
        field = [[self.FOG_SYMBOL for _ in range(self.model.width)] for _ in range(self.model.height)]
        for row in self.model.cells:
            for cell in row:
                if cell.vision == CellVision.VISIBLE:
                    field[cell.row][cell.column] = \
                        self.FLOOR_SYMBOL if cell.cell_type == CellType.FLOOR else self.WALL_SYMBOL

        for game_object in self.model.game_objects:
            if game_object.cell.vision == CellVision.VISIBLE and isinstance(game_object, Door):
                field[game_object.cell.row][game_object.cell.column] = self.DOOR_SYMBOL

        for i in range(min(self.model.height, self.height)):
            for j in range(min(self.model.width, self.width)):
                console.addstr(i, j, field[i][j])

        self._print_with_read_color(console, self.dungeon.player.cell.row, self.dungeon.player.cell.column,
                                    self.PLAYER_SYMBOL)
