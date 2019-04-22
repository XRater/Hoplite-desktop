from src.model.equipment.equipment import Equipment


class Armor(Equipment):
    def __init__(self, cell, damage_boost=0, damage_absorption=3):
        super(Armor, self).__init__(cell, Equipment.EquipmentType.ARMOR,
                                    damage_boost=damage_boost,
                                    damage_absorption=damage_absorption)
