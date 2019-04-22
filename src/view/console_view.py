import curses

from src.model.cell import CellType, CellVision
from src.model.door import Door


class ConsoleView(object):
    """
    A very simple console view for a game. It is using curces library.
    """
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
    _vision_color = 2
    _fog_color = 3

    def __init__(self, controller, dungeon):
        self.controller = controller
        self.dungeon = dungeon
        self.model = dungeon.field

    def start(self):
        """
        A method that starts game cycle. It reads user's input, pass it to controller and than draws.
        Note that after this method is called you can't print anything else in stdout.
        """
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
        footer = 'Press {} to exit'.format(self.QUIT_BUTTON)
        console.addstr(self.height - 1, 0, footer)
        console.addstr(self.height - 1, len(footer), ' ' * (self.width - len(footer) - 1))

    def _draw_menu(self, console):
        command = 0

        console.clear()
        console.refresh()

        curses.start_color()
        curses.init_pair(self._red_color, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(self._vision_color, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(self._fog_color, curses.COLOR_WHITE, curses.COLOR_BLACK)

        while command != ord(self.QUIT_BUTTON):
            console.clear()
            self.height, self.width = console.getmaxyx()

            if command == ord(' '):
                self._start_game(console)
                break

            start_x_title = self.width // 2 - len(self.WELCOME_STRING) // 2 - len(self.WELCOME_STRING) % 2
            start_x_subtitle = self.width // 2 - len(self.INSTRUCTION_STRING) // 2 - len(self.INSTRUCTION_STRING) % 2
            start_y = self.height // 2 - 2

            self._print_with_custom_color(console, start_y, start_x_title, self.WELCOME_STRING, self._red_color)
            self._print_with_custom_color(console, start_y + 1, start_x_subtitle, self.INSTRUCTION_STRING,
                                          self._red_color)

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

    def _draw_game(self, console):
        self.height, self.width = console.getmaxyx()

        player_row = self.dungeon.player.cell.row
        player_col = self.dungeon.player.cell.column
        start_row = max(player_row - self.height // 2, 0)
        start_col = max(player_col - self.width // 2, 0)

        self.draw_field(console, start_row, start_col)

    def draw_field(self, console, start_row, start_col):
        field = [[self.FOG_SYMBOL for _ in range(self.model.width)] for _ in range(self.model.height)]
        for row in self.model.cells:
            for cell in row:
                if not cell.vision == CellVision.UNSEEN:
                    field[cell.row][cell.column] = \
                        self.FLOOR_SYMBOL if cell.cell_type == CellType.FLOOR else self.WALL_SYMBOL

        for game_object in self.model.game_objects:
            if not game_object.cell.vision == CellVision.UNSEEN and isinstance(game_object, Door):
                field[game_object.cell.row][game_object.cell.column] = self.DOOR_SYMBOL

        for i in range(0, self.height):
            for j in range(0, self.width):
                if i + start_row < self.model.height and j + start_col < self.model.width:
                    color = self.detect_color(i + start_row, j + start_col)
                    self._print_with_custom_color(console, i, j, field[i + start_row][j + start_col], color)

        self._print_with_custom_color(console, self.dungeon.player.cell.row - start_row,
                                      self.dungeon.player.cell.column - start_col,
                                      self.PLAYER_SYMBOL, self._red_color)

    @staticmethod
    def _print_with_custom_color(console, y, x, text, color):
        console.attron(curses.color_pair(color))
        console.attron(curses.A_BOLD)
        console.addstr(y, x, text)
        console.attroff(curses.color_pair(color))
        console.attroff(curses.A_BOLD)

    def detect_color(self, row, col):
        return self._vision_color if self.model.cells[row][col].vision == CellVision.VISIBLE else self._fog_color
