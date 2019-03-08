class Door(object):
    def __init__(self, first_room, second_room, cell):
        self.cell = cell
        self._first_room = first_room
        self._second_room = second_room
