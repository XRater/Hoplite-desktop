from src.model.game_object import GameObject


class Door(GameObject):
    def __init__(self, cell, is_locked=False):
        super().__init__(cell)
        self.is_locked = is_locked
