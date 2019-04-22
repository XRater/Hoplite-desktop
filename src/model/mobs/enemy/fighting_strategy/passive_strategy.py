from src.model.mobs.enemy.fighting_strategy.fighting_strategy import FightingStrategy
from src.model.mobs.enemy.enemy_turn import EnemyTurn


class PassiveStrategy(FightingStrategy):
    def attack_player(self, field, current_cell):
        player_cell = field.find_player().cell
        player_position = player_cell.row, player_cell.column
        current_position = current_cell.row, current_cell.column
        if abs(player_position[0] - current_position[0]) + abs(player_position[1] - current_position[1]) == 1:
            return [EnemyTurn.get_turn_by_move(player_position[0] - current_position[0],
                                               player_position[1] - current_position[1])]
        return []
