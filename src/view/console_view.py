import curses
from enum import Enum, auto

from src.controller.turn_result import TurnResult
from src.model.cell import CellType, CellVision
from src.model.door import Door
from src.model.mobs.enemy import Enemy


class GameOver(Enum):
    EXIT_GAME = auto()
    YOU_DIED = auto()


class ConsoleView(object):
    """
    A very simple console view for a game. It is using curces library.
    """
    QUIT_BUTTON = 'q'
    WELCOME_STRING = 'Hi there! Check out our best game!\n'
    INSTRUCTION_STRING = 'Press SPACE to continue.\n'
    YOU_DIED_STRING = 'You died:( Game over.\n'
    SAVING_SCREEN = "Please enter file where you want to save this game and press ENTER.\n" \
                    "Empty line if yoy don't want to save.\n"
    WALL_SYMBOL = '#'
    FLOOR_SYMBOL = '.'
    FOG_SYMBOL = '~'
    DOOR_SYMBOL = 'O'
    PLAYER_SYMBOL = '@'
    ENEMY_SYMBOL = '&'

    _red_color = 1
    _fog_color = 2

    def __init__(self, controller, dungeon):
        self.controller = controller
        self.dungeon = dungeon
        self.model = dungeon.field
        self.movements = {curses.KEY_RIGHT: controller.pressed_right,
                          curses.KEY_LEFT: controller.pressed_left,
                          curses.KEY_UP: controller.pressed_up,
                          curses.KEY_DOWN: controller.pressed_down}

    def start(self):
        """
        A method that starts game cycle. It reads user's input, pass it to controller and than draws.
        Note that after this method is called you can't print anything else in stdout.
        """
        curses.wrapper(self._draw_menu)

    def _start_game(self, console):
        command = 0

        self._draw_game(console)

        while command != ord(self.QUIT_BUTTON):
            self.height, self.width = console.getmaxyx()

            if command in self.movements:
                result = self.movements[command]()
                if result == TurnResult.GAME_OVER:
                    return GameOver.YOU_DIED
                if result == TurnResult.TURN_ACCEPTED:
                    self._draw_game(console)
                if result == TurnResult.BAD_TURN:
                    # Nothing should be done here
                    pass

            command = console.getch()

        return GameOver.EXIT_GAME

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
        curses.init_pair(self._fog_color, curses.COLOR_CYAN, curses.COLOR_BLACK)

        while command != ord(self.QUIT_BUTTON):
            console.clear()
            self.height, self.width = console.getmaxyx()

            if command == ord(' '):
                game_result = self._start_game(console)
                if game_result == GameOver.YOU_DIED:
                    return self._print_game_over(console)
                else:
                    return self._process_exit(console)

            self._print_in_the_middle(console, self.height // 2 - 2, self.WELCOME_STRING, self._red_color)
            self._print_in_the_middle(console, self.height // 2 - 1, self.INSTRUCTION_STRING, self._red_color)

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
        console.clear()
        field = [[self.FOG_SYMBOL for _ in range(self.model.width)] for _ in range(self.model.height)]
        for row in self.model.cells:
            for cell in row:
                if not cell.vision == CellVision.UNSEEN:
                    field[cell.row][cell.column] = \
                        self.FLOOR_SYMBOL if cell.cell_type == CellType.FLOOR else self.WALL_SYMBOL

        for game_object in self.model.game_objects:
            if not game_object.cell.vision == CellVision.UNSEEN and isinstance(game_object, Door):
                field[game_object.cell.row][game_object.cell.column] = self.DOOR_SYMBOL
            if not game_object.cell.vision == CellVision.UNSEEN and isinstance(game_object, Enemy):
                field[game_object.cell.row][game_object.cell.column] = self.ENEMY_SYMBOL

        for i in range(min(self.model.height, self.height)):
            for j in range(min(self.model.width, self.width)):
                if self.model.cells[i][j].vision == CellVision.FOGGED:
                    self._print_with_custom_color(console, i, j, field[i][j], self._fog_color)
                else:
                    console.addstr(i, j, field[i][j])

        self._print_with_custom_color(console, self.dungeon.player.cell.row, self.dungeon.player.cell.column,
                                      self.PLAYER_SYMBOL, self._red_color)

        self._print_footer(console)
        console.refresh()

    def _print_game_over(self, console):
        self._print_in_the_middle(console, self.height // 2 - 2, self.YOU_DIED_STRING, self._red_color)
        self._print_footer(console)
        console.refresh()

        char = None
        while char != ord(self.QUIT_BUTTON):
            char = console.getch()

    def _print_in_the_middle(self, console, y, text, color):
        start_x_title = self.width // 2 - len(text) // 2 - len(text) % 2
        self._print_with_custom_color(console, y, start_x_title, text, color)

    @staticmethod
    def _print_with_custom_color(console, y, x, text, color):
        console.attron(curses.color_pair(color))
        console.attron(curses.A_BOLD)
        console.addstr(y, x, text)
        console.attroff(curses.color_pair(color))
        console.attroff(curses.A_BOLD)
