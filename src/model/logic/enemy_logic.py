import logging

from src.model.mobs.enemy.enemy_turn import EnemyTurn


class EnemyLogic:

    def __init__(self, logic, dungeon):
        self._logic = logic
        self._dungeon = dungeon

    # Making turn as enemy
    def make_enemy_turn(self, enemy):
        players = self._dungeon.field.find_players()
        move_strategy = enemy.create_turn(self._dungeon.field)
        for action in move_strategy:
            logging.info(action)
            delta_row, delta_column = EnemyTurn.get_deltas_by_turn(action)
            target_cell = self._dungeon.field.cells[enemy.cell.row + delta_row][enemy.cell.column + delta_column]
            for player in players:
                if player.cell == target_cell:
                    self.attack_player(player, enemy)
            if not self._dungeon.field.has_units_on_cell(target_cell):
                logging.info(f"Enemy moved to cell {target_cell}")
                enemy.cell = target_cell

    # Attack player as enemy
    def attack_player(self, player, enemy):
        damage = enemy.get_damage()
        logging.info(f"Enemy attacked player for damage {damage}")
        self._logic.fight_logic.attack_unit(enemy, player, damage)

    def kill(self, enemy):
        self._dungeon.remove_game_object(enemy)
        self.drop_loot(enemy)

    def drop_loot(self, enemy):
        for equipment in enemy.drop_loot:
            equipment.cell = enemy.cell
            self._dungeon.field.game_objects.append(equipment)
            logging.info("Dropped equipment")
