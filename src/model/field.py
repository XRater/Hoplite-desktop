from src.model.mobs.enemy.fighting_strategy.aggressive_strategy import AggressiveStrategy
from src.model.mobs.enemy.fighting_strategy.passive_strategy import PassiveStrategy
from src.model.mobs.enemy.fighting_strategy.cowardly_strategy import CowardlyStrategy
from src.model.equipment.armor import Armor
from src.model.equipment.weapon import Weapon
from src.model.equipment.helmet import Helmet
from src.model.equipment.shoes import Shoes
from src.model.cell import Cell, CellType
from src.model.door import Door
from src.model.mobs.enemy.enemy import Enemy
from src.model.player import Player
from src.model.room import Room

from random import randint, shuffle


class Field(object):
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rooms = []
        self.game_objects = []
        self.cells = [[Cell(row, column) for column in range(width)] for row in range(height)]
        self._generate_content()

    def find_player(self, player_id=None):
        """
        :return: player
        """
        players = [player for player in self.game_objects if isinstance(player, Player) and
                   (player_id is None or player.id == player_id)]
        assert len(players) == 1
        return players[0]

    def get_room_for_cell(self, cell):
        """
        :param cell: to look for
        :return: room containing target cell. Returns None if there is no such room
        """
        for room in self.rooms:
            if room.contains_cell(cell):
                return room
        return None

    # Checks if cell has units on it
    def has_units_on_cell(self, cell):
        objects_on_cell = self.get_object_for_cell(cell)
        for game_object in objects_on_cell:
            if isinstance(game_object, Enemy):
                return True
        return self.find_player().cell == cell

    def get_object_for_cell(self, cell):
        object_on_cell = []
        for game_object in self.game_objects:
            if game_object.cell == cell:
                object_on_cell.append(game_object)
        return object_on_cell

    def check_is_field(self, position):
        row, column = position
        if row < 0 or column < 0 or row > self.height or column > self.width:
            return False
        return self.cells[row][column].cell_type == CellType.FLOOR

    def get_enemies(self):
        enemies = []
        for game_object in self.game_objects:
            if isinstance(game_object, Enemy):
                enemies.append(game_object)
        return enemies

    # Field generation
    def _generate_content(self, min_room_size=2, max_room_size=8, rooms_unitedness=None,
                          wall_percent=25, min_enemies_amount=8, max_enemies_amount=16):
        rooms_dict = self._generate_rooms_grid(min_room_size, max_room_size)
        self._unite_rooms(rooms_dict, max_room_size, wall_percent)
        self.post_player()

        if not self._can_build_tree():
            self._cleanup_contents()
            self._generate_content(min_room_size, max_room_size, rooms_unitedness, wall_percent)
            return

        self._generate_doors()
        self._post_enemies(min_enemies_amount, max_enemies_amount)

    def _generate_rooms_grid(self, min_room_size, max_room_size):
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

        return rooms_dict

    def _unite_rooms(self, rooms_dict, max_room_size, wall_percent):
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

    def post_player(self):
        while True:
            player_room_ind = randint(0, len(self.rooms) - 1)
            room = self.rooms[player_room_ind]
            player_from_coords = room.corner_row, room.corner_column
            player_to_coords = player_from_coords[0] + room.height - 1, player_from_coords[1] + room.width - 1
            player_cell = self.cells[randint(player_from_coords[0], player_to_coords[0])][
                randint(player_from_coords[1], player_to_coords[1])]
            for game_object in self.game_objects:
                if game_object.cell.column == player_cell.column and game_object.cell.row == player_cell.row and \
                        isinstance(game_object, Player):
                    continue
            player = Player(player_cell)
            self.game_objects.append(player)
            return player

    def _generate_doors(self):
        for first_room, second_room in self.neighbour_rooms:
            type, s, range_min, range_max = self.rooms[first_room].get_common_range(self.rooms[second_room])
            if type == 'row':
                self.game_objects.append(Door(self.cells[randint(range_min, range_max)][s]))
            else:
                self.game_objects.append(Door(self.cells[s][randint(range_min, range_max)]))

        for door in self.game_objects:
            if isinstance(door, Door):
                door.cell.cell_type = CellType.FLOOR

    def _post_enemies(self, min_enemies_amount, max_enemies_amount):
        enemies_amount = randint(min_enemies_amount, max_enemies_amount)
        strategies = [AggressiveStrategy, PassiveStrategy, CowardlyStrategy]
        for _ in range(enemies_amount):
            position = -1, -1
            is_used = False
            while is_used or not self.check_is_field(position):
                position = randint(0, self.height - 1), randint(0, self.width - 1)
                is_used = False
                for obj in self.game_objects:
                    if obj.cell.row == position[0] and obj.cell.column == position[1]:
                        is_used = True
                        break
            strategy_number = randint(0, len(strategies) - 1)
            enemy = Enemy(self.cells[position[0]][position[1]])
            enemy.set_fighting_strategy(strategies[strategy_number]())
            drop_loot_amount = randint(0, 2)
            equipment = [Helmet(None), Armor(None), Weapon(None), Shoes(None)]
            shuffle(equipment)
            for ind in range(drop_loot_amount):
                enemy.add_drop_loot(equipment[ind])
            self.game_objects.append(enemy)

    def _cleanup_contents(self):
        self.rooms = []
        self.game_objects = []
        for cells_row in self.cells:
            for cell in cells_row:
                cell.cell_type = CellType.WALL

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
