import src.view.console_view_utils as utils
from src.model.cell import CellVision, CellType
from src.model.door import Door
from src.model.equipment.equipment import Equipment
from src.model.mobs.enemy.enemy import Enemy
from src.model.player import Player
from src.view.console_view import ConsoleView


class GameView(object):
    """A view that draws game field."""
    WALL_SYMBOL = '#'
    FLOOR_SYMBOL = '.'
    FOG_SYMBOL = '~'
    DOOR_SYMBOL = 'O'
    PLAYER_SYMBOL = '@'
    ENEMY_SYMBOL = '&'
    LOOT_SYMBOL = '!'

    def __init__(self, console):
        self.console = console
        # self.model = model
        # self.dungeon = dungeon
        self.height, self.width = self.console.getmaxyx()

    def draw_game(self, player_id, dungeon):
        """Method for drawing field."""
        self.console.clear()
        self.height, self.width = self.console.getmaxyx()

        player = list(filter(lambda p: isinstance(p, Player) and p.id == player_id, dungeon.field.game_objects))[0]
        player_row = player.cell.row
        player_col = player.cell.column
        start_row = max(player_row - self._get_effective_height() // 2, 0)
        start_col = max(player_col - self.width // 2, 0)

        self._draw_field(self.console, start_row, start_col, dungeon, player)

    def _draw_field(self, console, start_row, start_col, dungeon, player):
        model = dungeon.field
        field = [[self.FOG_SYMBOL for _ in range(model.width)] for _ in range(model.height)]
        for row in model.cells:
            for cell in row:
                if not cell.vision == CellVision.UNSEEN:
                    field[cell.row][cell.column] = \
                        self.FLOOR_SYMBOL if cell.cell_type == CellType.FLOOR else self.WALL_SYMBOL

        for game_object in model.game_objects:
            if not game_object.cell.vision == CellVision.UNSEEN:
                if isinstance(game_object, Door):
                    field[game_object.cell.row][game_object.cell.column] = self.DOOR_SYMBOL
                if isinstance(game_object, Enemy):
                    field[game_object.cell.row][game_object.cell.column] = self.ENEMY_SYMBOL
                if isinstance(game_object, Equipment):
                    field[game_object.cell.row][game_object.cell.column] = self.LOOT_SYMBOL

        for i in range(0, self._get_effective_height()):
            for j in range(0, self.width):
                if i + start_row < model.height and j + start_col < model.width:
                    color = self._detect_color(model.cells[i + start_row][j + start_col])
                    utils.print_with_custom_color(console, i, j, field[i + start_row][j + start_col], color)

        utils.print_with_custom_color(console, player.cell.row - start_row,
                                      player.cell.column - start_col,
                                      self.PLAYER_SYMBOL, ConsoleView.RED_COLOR)

        self._print_hp(player)
        utils.print_footer(console, self.height, self.width)
        console.refresh()

    def _get_effective_height(self):
        return self.height - 2

    def _detect_color(self, cell):
        return ConsoleView.VISION_COLOR if cell.vision == CellVision.VISIBLE else \
            ConsoleView.FOG_COLOR

    def _print_hp(self, player):
        hp = f'Health: {player.health} Damage: {player.get_damage()} Armor: {player.get_damage_absorption()} Level: {player.level}'
        self.console.addstr(self.height - 2, 0, hp)
