from src.model.mobs.fighting_strategy.fighting_strategy import FightingStrategy
from src.model.cell import CellType
from src.model.mobs.enemy_turn import EnemyTurn
from random import randint


class AggressiveStrategy(FightingStrategy):
    def attack_player(self, field, current_cell):
        player_cell = field.find_player().cell
        if field.get_room_for_cell(player_cell) != field.get_room_for_cell(current_cell):
            return []
        player_position = player_cell.row, player_cell.column
        current_position = current_cell.row, current_cell.column
        possible_cells = AggressiveStrategy._get_possible_cells_to_move(field, current_position, player_position)
        if len(possible_cells) == 0:
            return []
        move_number = randint(0, len(possible_cells) - 1)
        cell_to_move_x, cell_to_move_y = possible_cells[move_number]
        return [EnemyTurn.get_turn_by_move(cell_to_move_x - current_position[0],
                                           cell_to_move_y - current_position[1])]

    @staticmethod
    def _get_possible_cells_to_move(field, position, player_position):
        d_row, d_column = player_position[0] - position[0], player_position[1] - position[1]
        cells_to_move = []
        if d_row != 0:
            cells_to_move.append((position[0] + d_row // abs(d_row), position[1]))
        if d_column != 0:
            cells_to_move.append((position[0], position[1] + d_column // abs(d_column)))
        return [position for position in cells_to_move if field[position[0]][position[1]].cell_type == CellType.FLOOR]
