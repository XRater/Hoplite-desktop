from src.model.cell import Cell


class Field(object):
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rooms = []
        self.game_objects = []
        self.cells = [[Cell(row, column) for row in range(height)] for column in range(width)]
        self._generate_content()

    def _generate_content(self, debug=True):
        if debug:
            k = 5
            rows = [1 + row * ((self.height - 1) // k) for row in range(k)]
            rows.append(self.height)
            columns = [1 + column * ((self.width - 1) // k) for column in range(k)]
            columns.append(self.width)

            for row_ind, row in enumerate(rows[:-1]):
                for col_ind, col in (columns[:-1]):
                    height = rows[row_ind + 1] - row - 1
                    width = columns[col_ind + 1] - col - 1
                    self.rooms[(row, col)] = Room(height, width)

            for row_ind, row in enumerate(rows[:-2]):
                for col_ind, col in enumerate((columns[:-2])):
                    height = rows[row_ind + 1] - row - 1
                    width = columns[col_ind + 1] - col - 1
                    cur_room = self.rooms[(row, col)]
                    down_room = self.rooms[(row + height + 1, col)]
                    right_room = self.rooms[(row, col + width + 1)]

                    down_room_coords = (row + height, col + width // 2)
                    right_room_coords = (row + height // 2, col + width)
                    self._add_door(cur_room, right_room, row + height // 2, col + width)
                    self._add_door(cur_room, down_room, row + height, col + width // 2)

                    cur_room.add_door(cur_room.height, width // 2, self.doors[down_room_coords])
                    down_room.add_door(0, width // 2, self.doors[down_room_coords])

                    cur_room.add_door(cur_room.height // 2, width, self.doors[right_room_coords])
                    right_room.add_door(height // 2, 0, self.doors[right_room_coords])
        else:
            pass

    def _add_door(self, first_room, second_room, row, column):
        new_door = Door(first_room,
                        second_room,
                        None)
        new_door.cell = Cell(0, 0, new_door)
        self.doors[(row, column)] = new_door
