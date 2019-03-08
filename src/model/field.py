class Field(object):
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rooms = {}
        self.doors = {}
        self.game_objects = {}
        self._generate_content()

    def _generate_content(self):
        pass
