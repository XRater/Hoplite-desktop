import logging
import pickle

from src.model.field import Field
from src.model.logic import Logic
from src.view.view import View


class Controller(object):
    def __init__(self, field_file=None):
        if field_file is not None:
            with open(field_file, 'rb') as file:
                self._model_data = pickle.load(file)
        else:
            self._model_data = Field(50, 50)
        self._logic = Logic(self._model_data)
        self._view = View(self, self._model_data)

        logging.basicConfig(filename='game.log', format='%(levelname)s:%(message)s', level=logging.INFO)

    def start(self):
        self._view.start()

    def pressed_right(self):
        self._process_turn(lambda: self._logic.move_player(1, 0))

    def pressed_left(self):
        self._process_turn(lambda: self._logic.move_player(-1, 0))

    def pressed_up(self):
        self._process_turn(lambda: self._logic.move_player(0, -1))

    def pressed_down(self):
        self._process_turn(lambda: self._logic.move_player(0, 1))

    def _process_turn(self, f):
        result = f()
        if result:
            self._logic.make_turn()
