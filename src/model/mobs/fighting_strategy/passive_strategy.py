from src.model.mobs.fighting_strategy.fighting_strategy import FightingStrategy


class PassiveStrategy(FightingStrategy):
    def attack_player(self, field, current_cell):
        return []