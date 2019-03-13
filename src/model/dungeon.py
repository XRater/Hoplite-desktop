class Dungeon(object):
    def __init__(self, field):
        self.field = field
        self.player = self.field.find_player()
