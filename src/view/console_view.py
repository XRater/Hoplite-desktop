import curses
from enum import Enum, auto

import src.view.console_view_utils as utils
from src.controller.direction import Direction
from src.controller.move_command import MoveCommand
from src.controller.turn_result import TurnResult


class GameOver(Enum):
    EXIT_GAME = auto()
    YOU_DIED = auto()


class ConsoleView(object):
    """
    A very simple console view for a game. It is using curces library.
    """
    QUIT_BUTTON = 'q'
    INVENTORY_BUTTON = 'i'
    WELCOME_STRING = 'Hi there! Check out our best game!\n'
    INSTRUCTION_STRING = 'Press SPACE to continue.\n'
    YOU_DIED_STRING = 'You died:( Game over.\n'
    SAVING_SCREEN = "Please enter file where you want to save this game and press ENTER.\n" \
                    "Empty line if you don't want to save.\n"

    RED_COLOR = 1
    VISION_COLOR = 2
    FOG_COLOR = 3

    def __init__(self, controller, dungeon):
        self.controller = controller
        self.dungeon = dungeon
        self.model = dungeon.field
        self.movements = {curses.KEY_RIGHT: Direction.RIGHT,
                          curses.KEY_LEFT: Direction.LEFT,
                          curses.KEY_UP: Direction.UP,
                          curses.KEY_DOWN: Direction.DOWN}

    def start(self):
        """
        A method that starts game cycle. It reads user's input, pass it to controller and than draws.
        Note that after this method is called you can't print anything else in stdout.
        """
        curses.wrapper(self._draw_menu)

    def _start_game(self, console):
        from src.view.game_view import GameView
        from src.view.inventory_view import InventoryView

        game = GameView(console, self.model, self.dungeon)
        inventory = InventoryView(console, self.controller)

        action = 0

        game.draw_game()

        while action != ord(self.QUIT_BUTTON):
            self.height, self.width = console.getmaxyx()

            if action in self.movements:
                result = self.controller.process_user_command(MoveCommand(self.movements[action]))
                if result == TurnResult.GAME_OVER:
                    return GameOver.YOU_DIED
                if result == TurnResult.TURN_ACCEPTED:
                    game.draw_game()
                if result == TurnResult.BAD_TURN:
                    # Nothing should be done here
                    pass

            elif action == ord(self.INVENTORY_BUTTON):
                inventory.draw()
                game.draw_game()

            action = console.getch()

        return GameOver.EXIT_GAME

    def _draw_menu(self, console):
        command = 0

        console.clear()
        console.refresh()

        curses.start_color()
        curses.init_pair(self.RED_COLOR, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(self.VISION_COLOR, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(self.FOG_COLOR, curses.COLOR_WHITE, curses.COLOR_BLACK)

        while command != ord(self.QUIT_BUTTON):
            console.clear()
            self.height, self.width = console.getmaxyx()

            if command == ord(' '):
                game_result = self._start_game(console)
                if game_result == GameOver.YOU_DIED:
                    return self._print_game_over(console)
                else:
                    return self._process_exit(console)

            utils.print_in_the_middle(console, self.height // 2 - 2, self.width, self.WELCOME_STRING, self.RED_COLOR)
            utils.print_in_the_middle(console, self.height // 2 - 1, self.width, self.INSTRUCTION_STRING,
                                      self.RED_COLOR)

            utils.print_footer(console, self.height, self.width)

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

    def _print_game_over(self, console):
        utils.print_in_the_middle(console, self.height // 2 - 2, self.width, self.YOU_DIED_STRING, self.RED_COLOR)
        utils.print_footer(console, self.height, self.width)
        console.refresh()

        char = None
        while char != ord(self.QUIT_BUTTON):
            char = console.getch()
