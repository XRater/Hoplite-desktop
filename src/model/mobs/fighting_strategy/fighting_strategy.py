class FightingStrategy(object):
    """
    Fighting strategy
    """
    def attack_player(self, field, current_cell):
        """
        Describes enemy turn according to the certain strategy
        :param field: dungeon field
        :param current_cell: current enemy position
        :return: list of EnemyTurn objects
        """
        raise NotImplementedError()
