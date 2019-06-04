from src.model.player import Player


class Dungeon(object):
    def __init__(self, field):
        self.field = field
        self.player = self.field.find_player()

    def remove_game_object(self, game_object):
        if isinstance(game_object, Player):
            return
        self.field.game_objects.remove(game_object)

    def add_new_player(self):
        player = self.field.post_player()
        return player.id
