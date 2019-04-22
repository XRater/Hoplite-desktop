import logging


class FightLogic:

    def __init__(self, logic, dungeon):
        self._logic = logic
        self._dungeon = dungeon

    def attack_unit(self, unit, damage):
        logging.info("Dealing {damage} damage to unit".format(damage=damage))
        if unit.health > damage:
            unit.health = unit.health - damage
        else:
            unit.health = 0
            logging.info("Unit died")
            self._dungeon.remove_game_object(unit)