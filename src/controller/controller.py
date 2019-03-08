import pickle

from src.model.field import Field
from src.model.logic import Logic


class Controller(object):
    def __init__(self, field_file=None):
        if field_file is not None:
            with open(field_file, 'rb') as file:
                self._logic = Logic(pickle.load(file))
        else:
            self._logic = Logic(Field(50, 50))

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
