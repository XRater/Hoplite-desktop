from src.model.door import Door
from src.model.mobs.enemy.enemy_turn import EnemyTurn
from src.model.mobs.enemy.fighting_strategy.fighting_strategy import FightingStrategy


class CowardlyStrategy(FightingStrategy):
    def create_turn(self, field, current_cell):
        player_cell = field.find_players()[0].cell  # TODO
        player_position = player_cell.row, player_cell.column
        current_position = current_cell.row, current_cell.column
        if field.get_room_for_cell(player_cell) != field.get_room_for_cell(current_cell):
            return []
        possible_moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        cells_to_move = [(current_position[0] + move[0], current_position[1] + move[1]) for move in possible_moves]
        cells_to_move = list(zip(cells_to_move, possible_moves))
        cells_to_move = [(position, move) for position, move in cells_to_move if field.check_is_field(position)]
        moves = [(abs(position[0] - player_position[0]) + abs(position[1] - player_position[1]), move)
                 for position, move in cells_to_move]
        # Damn, where is my numpy
        max_dist = -1
        max_move = None
        for dist, move in moves:
            is_door = False
            if max_dist < dist:
                for obj in field.game_objects:
                    if isinstance(obj, Door) and obj.cell.row == current_position[0] + move[0] \
                            and obj.cell.column == current_position[1] + move[1]:
                        is_door = True
                        break
                if is_door:
                    break
                max_dist = dist
                max_move = move
        if max_move is None:
            return []
        return [EnemyTurn.get_turn_by_move(*max_move)]
