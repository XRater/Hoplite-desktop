import logging
import os
from time import strftime, gmtime

from src.controller.game_controller import GameController
from src.view.console_view import ConsoleView


class AppController:
    """A class that is responsible for starting the game and configuring settings."""
    LOGS_DIR = 'logs/'

    def __init__(self):
        self._set_up_logs()
        self._view = None

    def start(self):
        self._view = ConsoleView(self)
        self._view.start()

    def start_game(self, filename=None):
        controller = GameController(self._view, filename)
        controller.start()
        return controller

    def _set_up_logs(self):
        log_name = 'game_process' + strftime("%Y-%m-%d_%H-%M-%S", gmtime()) + '.log'
        if not os.path.exists(self.LOGS_DIR):
            os.makedirs(self.LOGS_DIR)
        logging.basicConfig(filename='logs/' + log_name, format='%(levelname)s:%(message)s', level=logging.INFO)