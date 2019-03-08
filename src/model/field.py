class Field(object):
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self._rooms = []
        self._doors = []
