from src.model.cell import Cell, CellType
from src.model.door import Door
from src.model.player import Player
from src.model.room import Room

from random import randint


class Field(object):
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rooms = []
        self.game_objects = []
        self.cells = [[Cell(row, column) for column in range(width)] for row in range(height)]
        self._generate_content(debug=False)

    def _generate_content(self, debug=True, min_room_size=2, max_room_size=8, rooms_unitedness=None,
                          wall_percent=25):
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
            rows = [1]
            while self.height >= rows[-1] + 2 * min_room_size + 3:
                rows.append(randint(rows[-1] + min_room_size + 1, min(self.height - min_room_size - 2,
                                                                      rows[-1] + max_room_size + 1)))
            rows.append(self.height)

            cols = [1]
            while self.width >= cols[-1] + 2 * min_room_size + 3:
                cols.append(randint(cols[-1] + min_room_size + 1, min(self.width - min_room_size - 2,
                                                                      cols[-1] + max_room_size + 1)))
            cols.append(self.width)

            rooms_dict = {}
            for row_ind, row in enumerate(rows[:-1]):
                for col_ind, col in enumerate(cols[:-1]):
                    height = rows[row_ind + 1] - row - 1
                    width = cols[col_ind + 1] - col - 1
                    rooms_dict[(row, col)] = Room(height, width, row, col)

            while True:
                rooms_to_union = []
                for coords, room in rooms_dict.items():
                    room_at_right_coords = (coords[0], coords[1] + room.width + 1)
                    if room_at_right_coords in rooms_dict and rooms_dict[room_at_right_coords].height == room.height \
                            and room.width + rooms_dict[room_at_right_coords].width + 1 <= 2 * max_room_size - 5:
                        rooms_to_union.append((coords, room_at_right_coords))

                    room_at_bottom_coords = (coords[0] + room.height + 1, coords[1])
                    if room_at_bottom_coords in rooms_dict and rooms_dict[room_at_bottom_coords].width == room.width \
                            and room.height + rooms_dict[room_at_bottom_coords].height + 1 <= 2 * max_room_size - 5:
                        rooms_to_union.append((coords, room_at_bottom_coords))

                if len(rooms_to_union) == 0:
                    break

                ind = randint(0, len(rooms_to_union) - 1)
                first_room, second_room = rooms_to_union[ind]
                if rooms_dict[first_room].height == rooms_dict[second_room].height and first_room[0] == second_room[0]:
                    rooms_dict[first_room].width += rooms_dict[second_room].width + 1
                else:
                    rooms_dict[first_room].height += rooms_dict[second_room].height + 1
                del rooms_dict[second_room]

            self.rooms = [room for room in rooms_dict.values() if randint(0, 100) > wall_percent
                          and room.height * room.width > 8]

            for room in self.rooms:
                for row in range(room.corner_row, room.corner_row + room.height):
                    for column in range(room.corner_column, room.corner_column + room.width):
                        self.cells[row][column].cell_type = CellType.FLOOR

            player_room_ind = randint(0, len(self.rooms) - 1)
            room = self.rooms[player_room_ind]
            player_from_coords = room.corner_row, room.corner_column
            player_to_coords = player_from_coords[0] + room.height, player_from_coords[1] + room.width
            self.game_objects.append(Player(self.cells[randint(player_from_coords[0], player_to_coords[0])]
                                            [randint(player_from_coords[1], player_to_coords[1])]))
            if not self._can_build_tree():
                self.rooms = []
                self.game_objects = []
                for cells_row in self.cells:
                    for cell in cells_row:
                        cell.cell_type = CellType.WALL

                self._generate_content(debug, min_room_size, max_room_size, rooms_unitedness, wall_percent)
                return

            print(len(self.rooms) - len(self.neighbour_rooms))
            for first_room, second_room in self.neighbour_rooms:
                type, s, range_min, range_max = self.rooms[first_room].get_common_range(self.rooms[second_room])
                if type == 'row':
                    self.game_objects.append(Door(self.cells[randint(range_min, range_max)][s]))
                else:
                    self.game_objects.append(Door(self.cells[s][randint(range_min, range_max)]))

    def _can_build_tree(self):
        edges = self._build_room_graph()
        was = [False for _ in range(len(self.rooms))]
        self.neighbour_rooms = []
        self._dfs(0, edges, was)
        for was_in_room in was:
            if not was_in_room:
                return False

        return True

    def _build_room_graph(self):
        edges = [[] for _ in self.rooms]
        for i, first_room in enumerate(self.rooms):
            for j, second_room in enumerate(self.rooms):
                if i == j:
                    continue
                if first_room.get_common_range(second_room) is not None:
                    edges[i].append(j)

        return edges

    def _dfs(self, current, edges, was):
        was[current] = True

        for next in edges[current]:
            if not was[next]:
                self.neighbour_rooms.append((current, next))
                self._dfs(next, edges, was)

    def find_player(self):
        return [player for player in self.game_objects if isinstance(player, Player)][0]


if __name__ == '__main__':
    field = Field(40, 80)
    for row in field.cells:
        for cell in row:
            if cell.cell_type == CellType.FLOOR:
                print('.', end='')
            else:
                is_door = False
                for game_object in field.game_objects:
                    if isinstance(game_object, Door) and cell.row == game_object.cell.row \
                            and cell.column == game_object.cell.column:
                        print('0', end='')
                        is_door = True
                        break
                if not is_door:
                    print('#', end='')
        print()
