import logging

from src.model.mobs.enemy.enemy import Enemy
from src.model.player import Player


class FightLogic:

    def __init__(self, logic, dungeon):
        self._logic = logic
        self._dungeon = dungeon

    def attack_unit(self, unit, target, damage):
        logging.info("Dealing {damage} damage to unit".format(damage=damage))
        if target.health > damage:
            target.health = target.health - damage
        else:
            target.health = 0
            logging.info("Unit died")
            if isinstance(target, Enemy):
                self._logic.enemy_logic.kill(target)
                if isinstance(unit, Player):
                    self._logic.player_logic.gain_experience(unit, target.get_experience())
