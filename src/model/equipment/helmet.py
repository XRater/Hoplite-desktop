from src.model.equipment.equipment import Equipment


class Helmet(Equipment):
    def __init__(self, cell, damage_boost=0, damage_absorption=20):
        super(Helmet, self).__init__(cell,
                                     'Helmet: {} damage boost, {} damage absorption'.format(damage_boost,
                                                                                            damage_absorption),
                                     Equipment.EquipmentType.HELMET,
                                     damage_boost=damage_boost,
                                     damage_absorption=damage_absorption)
