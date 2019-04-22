import logging
import pickle

from src.controller.turn_result import TurnResult
from src.model.dungeon import Dungeon
from src.model.field import Field
from src.model.logic.logic import Logic
from src.view.console_view import ConsoleView


class Controller(object):
    """It's a class that plays role of `C` in a standard MVC pattern."""

    def __init__(self, field_file=None):
        if field_file is not None:
            with open(field_file, 'rb') as file:
                self._dungeon = Dungeon(pickle.load(file))
                logging.info('Loading dungeon from file {}'.format(field_file))
        else:
            self._dungeon = Dungeon(Field(30, 50))
            logging.info('Initializing new dungeon')
        self._logic = Logic(self._dungeon)
        self._view = ConsoleView(self, self._dungeon)
        logging.info('Dungeon is completed')

    def start(self):
        self._view.start()

    def pressed_right(self):
        return self._process_turn(lambda: self._logic.move_player(0, 1))

    def pressed_left(self):
        return self._process_turn(lambda: self._logic.move_player(0, -1))

    def pressed_up(self):
        return self._process_turn(lambda: self._logic.move_player(-1, 0))

    def pressed_down(self):
        return self._process_turn(lambda: self._logic.move_player(1, 0))

    def save_field(self, filename):
        logging.info('Saving game to {}'.format(filename))
        with open(filename, 'wb') as file:
            pickle.dump(self._dungeon.field, file)

    def _process_turn(self, f):
        result = f()
        if result == TurnResult.TURN_ACCEPTED:
            logging.info("Turn was accepted. Waiting for new turn")
            return self._logic.make_turn()
        if result == TurnResult.GAME_OVER:
            logging.info("Game over")
        if result == TurnResult.BAD_TURN:
            logging.info("Turn was not valid")
        return result
