class Field(object):
    def __init__(self, height, width, field_file=None):
        if field_file is None:
            self.height = height
            self.width = width
            self.rooms = {}
            self.doors = {}
            self.game_objects = {}
            self._generate_content()
        else:
            pass

    def _generate_content(self):
        pass
