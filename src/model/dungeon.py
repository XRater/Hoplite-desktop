class Dungeon(object):
    def __init__(self, field):
        self.field = field
        self.player = self.field.find_player()

    def remove_game_object(self, game_object):
        self.field.game_objects.remove(game_object)