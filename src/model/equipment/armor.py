from src.model.equipment.equipment import Equipment


class Armor(Equipment):
    def __init__(self, cell, damage_boost=0, damage_absorption=30):
        super(Armor, self).__init__(cell,
                                    'Armor: {} damage boost, {} damage absorption'.format(damage_boost,
                                                                                          damage_absorption),
                                    Equipment.EquipmentType.ARMOR,
                                    damage_boost=damage_boost,
                                    damage_absorption=damage_absorption)
