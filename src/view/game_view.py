import src.view.console_view_utils as utils
from src.model.cell import CellVision, CellType
from src.model.door import Door
from src.model.mobs.enemy.enemy import Enemy
from src.view.console_view import ConsoleView


class GameView(object):
    WALL_SYMBOL = '#'
    FLOOR_SYMBOL = '.'
    FOG_SYMBOL = '~'
    DOOR_SYMBOL = 'O'
    PLAYER_SYMBOL = '@'
    ENEMY_SYMBOL = '&'

    def __init__(self, console, model, dungeon):
        self.console = console
        self.model = model
        self.dungeon = dungeon
        self.height, self.width = self.console.getmaxyx()

    def draw_game(self):
        self.console.clear()
        self.height, self.width = self.console.getmaxyx()

        player_row = self.dungeon.player.cell.row
        player_col = self.dungeon.player.cell.column
        start_row = max(player_row - self._get_effective_height() // 2, 0)
        start_col = max(player_col - self.width // 2, 0)

        self._draw_field(self.console, start_row, start_col)

    def _draw_field(self, console, start_row, start_col):
        field = [[self.FOG_SYMBOL for _ in range(self.model.width)] for _ in range(self.model.height)]
        for row in self.model.cells:
            for cell in row:
                if not cell.vision == CellVision.UNSEEN:
                    field[cell.row][cell.column] = \
                        self.FLOOR_SYMBOL if cell.cell_type == CellType.FLOOR else self.WALL_SYMBOL

        for game_object in self.model.game_objects:
            if not game_object.cell.vision == CellVision.UNSEEN and isinstance(game_object, Door):
                field[game_object.cell.row][game_object.cell.column] = self.DOOR_SYMBOL
            if not game_object.cell.vision == CellVision.UNSEEN and isinstance(game_object, Enemy):
                field[game_object.cell.row][game_object.cell.column] = self.ENEMY_SYMBOL

        for i in range(0, self._get_effective_height()):
            for j in range(0, self.width):
                if i + start_row < self.model.height and j + start_col < self.model.width:
                    color = self._detect_color(i + start_row, j + start_col)
                    utils.print_with_custom_color(console, i, j, field[i + start_row][j + start_col], color)

        utils.print_with_custom_color(console, self.dungeon.player.cell.row - start_row,
                                      self.dungeon.player.cell.column - start_col,
                                      self.PLAYER_SYMBOL, ConsoleView.RED_COLOR)

        self._print_hp()
        utils.print_footer(console, self.height, self.width)
        console.refresh()

    def _get_effective_height(self):
        return self.height - 2

    def _detect_color(self, row, col):
        return ConsoleView.VISION_COLOR if self.model.cells[row][col].vision == CellVision.VISIBLE else \
            ConsoleView.FOG_COLOR

    def _print_hp(self):
        hp = f'Health: {self.dungeon.player.health}'
        self.console.addstr(self.height - 2, 0, hp)
