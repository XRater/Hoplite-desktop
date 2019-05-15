import logging
import pickle

from src.controller.turn_result import TurnResult
from src.model.dungeon import Dungeon
from src.model.field import Field
from src.model.logic.logic import Logic


class GameController(object):
    """It's a class that plays role of `C` in a standard MVC pattern."""

    def __init__(self, view, field_file=None):
        if field_file is not None:
            with open(field_file, 'rb') as file:
                self._dungeon = Dungeon(pickle.load(file))
                logging.info('Loading dungeon from file {}'.format(field_file))
        else:
            self._dungeon = Dungeon(Field(30, 50))
            logging.info('Initializing new dungeon')
        self._logic = Logic(self._dungeon)
        self._view = view
        logging.info('Dungeon is completed')

    def start(self):
        # pass
        # self._view.start()
        self._view.draw(self._dungeon)
        self._view.get_turn()

    def process_user_command(self, command):
        self._view.block_input()

        result = command.execute(self._logic)
        if result == TurnResult.TURN_ACCEPTED:
            logging.info("Turn was accepted. Waiting for new turn")
            self._view.draw(self._dungeon)
            self.call_enemy_turn()
        if result == TurnResult.GAME_OVER:
            logging.info("Game over")
            self._view.game_over()
        if result == TurnResult.BAD_TURN:
            logging.info("Turn was not valid")
            self._view.get_turn()

    def call_enemy_turn(self):
        result = self._logic.make_turn()
        if result == TurnResult.TURN_ACCEPTED:
            self._view.draw(self._dungeon)
            self._view.get_turn()
        if result == TurnResult.GAME_OVER:
            logging.info("Game over")
            self._view.game_over()
        if result == TurnResult.BAD_TURN:
            raise Exception()

    def save_game(self, filename):
        logging.info('Saving game to {}'.format(filename))
        with open(filename, 'wb') as file:
            pickle.dump(self._dungeon.field, file)

    def save(self):
        pass
