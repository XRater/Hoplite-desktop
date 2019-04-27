import logging

from src.model.mobs.enemy.enemy_turn import EnemyTurn


class EnemyLogic:

    def __init__(self, logic, dungeon):
        self._logic = logic
        self._dungeon = dungeon

    # Making turn as enemy
    def make_enemy_turn(self, enemy):
        player = self._dungeon.player
        move_strategy = enemy.attack_player(self._dungeon.field)
        for action in move_strategy:
            logging.info(action)
            delta_row, delta_column = EnemyTurn.get_deltas_by_turn(action)
            target_cell = self._dungeon.field.cells[enemy.cell.row + delta_row][enemy.cell.column + delta_column]
            if player.cell == target_cell:
                self.attack_player(enemy)
            if not self._dungeon.field.has_units_on_cell(target_cell):
                logging.info(f"Enemy moved to cell {target_cell}")
                enemy.cell = target_cell

    # Attack player as enemy
    def attack_player(self, enemy):
        damage = enemy.get_damage()
        logging.info(f"Enemy attacked player for damage {damage}")
        self._logic.fight_logic.attack_unit(self._dungeon.player, damage)

    def kill(self, enemy):
        self._dungeon.remove_game_object(enemy)
        self.drop_loot(enemy)

    def drop_loot(self, enemy):
        for equipment in enemy.drop_loot:
            equipment.cell = enemy.cell
