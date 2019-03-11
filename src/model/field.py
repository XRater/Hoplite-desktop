from src.model.cell import Cell, CellType
from src.model.door import Door
from src.model.player import Player
from src.model.room import Room


class Field(object):
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rooms = []
        self.game_objects = []
        self.cells = [[Cell(row, column) for column in range(width)] for row in range(height)]
        self._generate_content(debug=True)

    def _generate_content(self, debug=True):
        if debug:
            k = 4
            rows = [1 + row * ((self.height - 1) // k) for row in range(k)]
            rows.append(self.height)
            columns = [1 + column * ((self.width - 1) // k) for column in range(k)]
            columns.append(self.width)

            for row_ind, row in enumerate(rows[:-1]):
                for col_ind, col in enumerate(columns[:-1]):
                    height = rows[row_ind + 1] - row - 1
                    width = columns[col_ind + 1] - col - 1
                    self.rooms.append(Room(height, width, row, col))
                    self.game_objects.append(Door(self.cells[row + height][col + width // 2]))
                    self.game_objects.append(Door(self.cells[row + height // 2][col + width]))

            for room in self.rooms:
                for row in range(room.corner_row, room.corner_row + room.height):
                    for column in range(room.corner_column, room.corner_column + room.width):
                        self.cells[row][column].cell_type = CellType.FLOOR

            for door in self.game_objects:
                door.cell.cell_type = CellType.FLOOR

            self.game_objects.append(Player(self.cells[1][1]))
        else:
            pass

    # Returns player
    def find_player(self):
        players = [player for player in self.game_objects if isinstance(player, Player)]
        assert len(players) == 1
        return players[0]

    # Returns room containing target cell. Returns None if there is no such room
    def get_room_for_cell(self, cell):
        for room in self.rooms:
            if room.contains_cell(cell):
                return room
        return None
