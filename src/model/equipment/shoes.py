from src.model.equipment.equipment import Equipment


class Shoes(Equipment):
    def __init__(self, cell, damage_boost=0, damage_absorption=10):
        super(Shoes, self).__init__(cell,
                                    'Shoes {} damage boost, {} damage absorption'.format(damage_boost,
                                                                                         damage_absorption),
                                    Equipment.EquipmentType.SHOES,
                                    damage_boost=damage_boost,
                                    damage_absorption=damage_absorption)
