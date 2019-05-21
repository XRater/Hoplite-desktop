import logging
import pickle
from multiprocessing.pool import Pool

from src.controller.turn_result import TurnResult


class ClientController(object):
    """It's a class that plays role of `C` in a standard MVC pattern."""

    def __init__(self, view, host, port):
        self.pool = Pool(processes=1)
        self._host = host
        self._port = port
        self._view = view
        # logging.info('Dungeon is completed')

    def start(self):
        self._view.render_dungeon(self._dungeon)
        self._view.get_turn()

    def process_user_command(self, command):
        self._view.block_input()

        def callback(result):
            result, dungeon = result
            self._dungeon = dungeon
            if result == TurnResult.TURN_ACCEPTED:
                logging.info("Turn was accepted. Waiting for new turn")
                self._view.render_dungeon(self._dungeon)
                self.call_enemy_turn()
            if result == TurnResult.GAME_OVER:
                logging.info("Game over")
                self._view.game_over()
            if result == TurnResult.BAD_TURN:
                logging.info("Turn was not valid")
                self._view.get_turn()

        self.pool.apply_async(command.execute, [self._logic], callback=callback)

    def call_enemy_turn(self):
        result = self._logic.make_turn()
        if result == TurnResult.TURN_ACCEPTED:
            self._view.render_dungeon(self._dungeon)
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
