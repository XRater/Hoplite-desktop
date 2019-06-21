from enum import Enum
from src.model.game_object import GameObject


class Equipment(GameObject):
    class EquipmentType(Enum):
        HELMET = 1
        ARMOR = 2
        SHOES = 3
        WEAPON = 4

    def __init__(self, cell, description, equipment_type, damage_boost, damage_absorption):
        super(Equipment, self).__init__(cell)
        self.equipment_type = equipment_type
        self.damage_boost = damage_boost
        self.damage_absorption = damage_absorption
        self.description = description
