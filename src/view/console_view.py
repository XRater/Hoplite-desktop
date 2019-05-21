import curses
from enum import Enum, auto

import src.view.console_view_utils as utils
from src.controller.direction import Direction
from src.controller.move_command import MoveCommand


class GameProcess(Enum):
    EXIT_GAME = auto()
    YOU_DIED = auto()
    IN_PROGRESS = auto()
    MENU = auto()


class GameState(Enum):
    WAITING_FOR_TURN = auto()
    BLOCKED = auto()


class ConsoleView(object):
    """
    A very simple console view for a game. It is using curces library.
    """
    QUIT_BUTTON = 'q'
    SAVE_BUTTON = 's'
    INVENTORY_BUTTON = 'i'
    WELCOME_STRING = 'Hi there! Check out our best game!\n'
    INSTRUCTION_STRING = 'Press SPACE to continue.\n'
    YOU_DIED_STRING = 'You died:( Game over.\n'
    SAVING_SCREEN = "Please enter file where you want to save this field and press ENTER.\n" \
                    "Empty line if you don't want to save.\n"

    RED_COLOR = 1
    VISION_COLOR = 2
    FOG_COLOR = 3

    def __init__(self, controller):
        self.app_controller = controller
        # self.dungeon = dungeon
        # self.model = dungeon.field
        self.movements = {curses.KEY_RIGHT: Direction.RIGHT,
                          curses.KEY_LEFT: Direction.LEFT,
                          curses.KEY_UP: Direction.UP,
                          curses.KEY_DOWN: Direction.DOWN}
        self._game_status = GameState.BLOCKED
        self._game_process = GameProcess.MENU
        self.game = None

    def get_turn(self):
        self._game_status = GameState.WAITING_FOR_TURN

    def block_input(self):
        self._game_status = GameState.BLOCKED

    def render_dungeon(self, dungeon):
        if self._game_process == GameProcess.IN_PROGRESS:
            self.game.draw_game(dungeon)

    def game_over(self):
        self._game_process = GameProcess.YOU_DIED

    def start(self):
        """
        A method that starts game cycle. It reads user's input, pass it to controller and than draws.
        Note that after this method is called you can't print anything else in stdout.
        """
        curses.wrapper(self._draw_screen)

    def _start_game_process(self, console):
        from src.view.game_view import GameView

        self.game = GameView(console)
        self.game_controller = self.app_controller.start_game()
        # self.model = self.controller
        # inventory = InventoryView(console, self.app_controller, self.dungeon)

        action = 0

        while action != ord(self.QUIT_BUTTON):
            if self._game_status == GameState.BLOCKED:
                action = console.getch()
                continue

            if action in self.movements:
                self.game_controller.process_user_command(MoveCommand(self.movements[action]))
                # if result == TurnResult.GAME_OVER:
                #     return GameOver.YOU_DIED
                # if result == TurnResult.TURN_ACCEPTED:
                #     self.game.draw_game()
                # if result == TurnResult.BAD_TURN:
                #     # Nothing should be done here
                #     pass

            elif action == ord(self.INVENTORY_BUTTON):
                # inventory.draw()
                self.game.draw_game()

            elif action == ord(self.SAVE_BUTTON):
                self.app_controller.save()

            if self._game_process == GameProcess.YOU_DIED:
                return
            action = console.getch()

        self._game_process = GameProcess.EXIT_GAME

    def _draw_screen(self, console):
        command = 0

        console.clear()
        console.refresh()

        curses.start_color()
        curses.init_pair(self.RED_COLOR, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(self.VISION_COLOR, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(self.FOG_COLOR, curses.COLOR_WHITE, curses.COLOR_BLACK)

        while True:
            if self._game_process == GameProcess.EXIT_GAME:
                self._print_exit_game(console)
                self._save_game(console)
                self._game_process = GameProcess.MENU
                self._print_main_menu(console)
            elif self._game_process == GameProcess.MENU:
                self._print_main_menu(console)
                if command == ord(' '):
                    self._game_process = GameProcess.IN_PROGRESS
                    self._start_game_process(console)
                    continue
                elif command == ord(self.QUIT_BUTTON):
                    break
            if self._game_process == GameProcess.YOU_DIED:
                self._print_game_over(console)
                self._wait_for_action(console)
                self._game_process = GameProcess.MENU
                self._print_main_menu(console)
            command = console.getch()

    def _print_exit_game(self, console):
        console.clear()
        curses.echo()
        console.addstr(0, 0, self.SAVING_SCREEN)

    def _save_game(self, console):
        filename = console.getstr(2, 0, 256).decode('utf-8')
        if filename.strip():
            self.game_controller.save_game(filename)

    def _print_main_menu(self, console):
        console.clear()
        height, width = console.getmaxyx()

        utils.print_in_the_middle(console, height // 2 - 2, width, self.WELCOME_STRING, self.RED_COLOR)
        utils.print_in_the_middle(console, height // 2 - 1, width, self.INSTRUCTION_STRING, self.RED_COLOR)
        utils.print_footer(console, height, width)

    def _print_game_over(self, console):
        console.clear()
        height, width = console.getmaxyx()

        utils.print_in_the_middle(console, height // 2 - 2, width, self.YOU_DIED_STRING, self.RED_COLOR)
        utils.print_footer(console, height, width)

    def _wait_for_action(self, console):
        console.getch()
