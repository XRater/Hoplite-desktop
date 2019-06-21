import curses
from enum import Enum, auto

import src.view.console_view_utils as utils
from src.controller.direction import Direction
from src.controller.move_command import MoveCommand
from src.model.player import Player
from src.view.inventory_view import InventoryView


class GameProcess(Enum):
    """
    Enum with different game states.
    """
    EXIT_GAME = auto()
    YOU_DIED = auto()
    IN_PROGRESS = auto()
    MENU = auto()


class GameState(Enum):
    """
    Enum with input state.
    """
    WAITING_FOR_TURN = auto()
    BLOCKED = auto()


class ConsoleView(object):
    """
    A very simple console view for a game. It is using curces library.
    """
    QUIT_BUTTON = 'q'
    INVENTORY_BUTTON = 'i'
    WELCOME_STRING = 'Hi there! Check out our best game!\n'
    INSTRUCTION_STRING = 'Press SPACE to start new session. ENTER to join an existing one\n'
    YOU_DIED_STRING = 'You died:( Game over.\n'
    SAVING_SCREEN = "Please enter file where you want to save this field and press ENTER.\n" \
                    "Empty line if you don't want to save.\n"

    RED_COLOR = 1
    VISION_COLOR = 2
    FOG_COLOR = 3

    def __init__(self, controller):
        self.app_controller = controller
        self.movements = {curses.KEY_RIGHT: Direction.RIGHT,
                          curses.KEY_LEFT: Direction.LEFT,
                          curses.KEY_UP: Direction.UP,
                          curses.KEY_DOWN: Direction.DOWN}
        self._game_status = GameState.BLOCKED
        self._game_process = GameProcess.MENU
        self.game = None
        self._dungeon = None  # Need to store it to draw dungeon after inventory view.
        self._player_id = None

    def get_turn(self):
        """
        Switch input state to WAITING_FOR_TURN
        """
        self._game_status = GameState.WAITING_FOR_TURN

    def block_input(self):
        """
        Switch input state to BLOCKED
        """
        self._game_status = GameState.BLOCKED

    def render_dungeon(self, dungeon):
        """
        Draw a dungeon that was passed.
        :param dungeon: dungeon to draw.
        :return: None
        """
        self._dungeon = dungeon  # Remember current dungeon
        if self._game_process == GameProcess.IN_PROGRESS:
            self.game.draw_game(self._get_current_player(), dungeon)

    def game_over(self):
        """
        Set game state to YOU_DIED
        """
        self._game_process = GameProcess.YOU_DIED

    def start(self):
        """
        A method that starts game cycle. It reads user's input, pass it to controller and than draws.
        Note that after this method is called you can't print anything else in stdout.
        """
        curses.wrapper(self._draw_screen)

    def _start_game_process(self, console, join_existing_session=False):
        from src.view.game_view import GameView

        self.game = GameView(console)
        self.game_controller = self.app_controller.start_game()
        inventory = InventoryView(console, self.game_controller)

        self._player_id, self._dungeon = self.game_controller.register(join_existing_session)
        self.render_dungeon(self._dungeon)
        action = 0

        while action != ord(self.QUIT_BUTTON):
            if self._game_status == GameState.BLOCKED:
                action = console.getch()
                continue
            if self._game_process == GameProcess.IN_PROGRESS:
                if action in self.movements:
                    self.game_controller.process_user_command(MoveCommand(self.movements[action]))

                elif action == ord(self.INVENTORY_BUTTON):
                    inventory.draw(self._get_current_player())
                    self.game.draw_game(self._get_current_player(), self._dungeon)

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
                    self._start_game_process(console, join_existing_session=False)
                    continue
                elif command == 10:  # 10 means ENTER. Doesn't work with curces.KEY_ENTER
                    self._game_process = GameProcess.IN_PROGRESS
                    self._start_game_process(console, join_existing_session=True)
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

    def _get_current_player(self):
        return list(filter(
            lambda p: isinstance(p, Player) and p.id == self._player_id, self._dungeon.field.game_objects))[0]
