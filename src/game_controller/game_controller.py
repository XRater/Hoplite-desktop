import logging
import os
from time import strftime, gmtime

from src.controller.controller import Controller


class GameController:
    LOGS_DIR = 'logs/'

    def __init__(self):
        self._set_up_logs()

    def start_game(self, filename=None):
        controller = Controller(filename)
        controller.start()

    def _set_up_logs(self):
        log_name = 'game_process' + strftime("%Y-%m-%d_%H-%M-%S", gmtime()) + '.log'
        if not os.path.exists(self.LOGS_DIR):
            os.makedirs(self.LOGS_DIR)
        logging.basicConfig(filename='logs/' + log_name, format='%(levelname)s:%(message)s', level=logging.INFO)