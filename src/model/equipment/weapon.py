from src.model.equipment.equipment import Equipment


class Weapon(Equipment):
    def __init__(self, cell, damage_boost=2, damage_absorption=5):
        super(Weapon, self).__init__(cell,
                                     'Weapon {} damage boost, {} damage absorption'.format(damage_boost,
                                                                                           damage_absorption),
                                     Equipment.EquipmentType.WEAPON,
                                     damage_boost=damage_boost,
                                     damage_absorption=damage_absorption)
