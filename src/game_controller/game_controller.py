import logging
import os
from time import strftime, gmtime

from src.controller.controller import Controller


class GameController:
    """A class that is responsible for starting the game and configuring settings."""
    LOGS_DIR = 'logs/'

    def __init__(self):
        self._set_up_logs()

    @staticmethod
    def start_game(filename=None):
        controller = Controller(filename)
        controller.start()

    def _set_up_logs(self):
        log_name = 'game_process' + strftime("%Y-%m-%d_%H-%M-%S", gmtime()) + '.log'
        if not os.path.exists(self.LOGS_DIR):
            os.makedirs(self.LOGS_DIR)
        logging.basicConfig(filename='logs/' + log_name, format='%(levelname)s:%(message)s', level=logging.INFO)