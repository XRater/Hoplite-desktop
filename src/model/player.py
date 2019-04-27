from src.model.equipment.equipment import Equipment
from src.model.game_object import GameObject


class Player(GameObject):
    INVENTORY_SIZE = 10

    def __init__(self, cell):
        super(Player, self).__init__(cell)
        self.health = 100
        self.base_damage = 9
        self.level = 1
        self.experience = 0
        self.equipment = {}
        self.inventory = []

    def get_damage_absorption(self):
        damage_absorption = 0
        for equipment in self.equipment.values():
            damage_absorption += equipment.damage_absorption
        return damage_absorption

    def get_damage(self):
        damage = self.base_damage + self.level
        for equipment in self.equipment.values():
            damage += equipment.damage_boost
        return damage

    def has_space_in_inventory(self):
        return len(self.inventory) < self.INVENTORY_SIZE

    def get_current_equipment_of_type(self, equipment_type):
        return self.equipment[equipment_type] if equipment_type in self.equipment else None

    def is_alive(self):
        return self.health > 0

    def __str__(self):
        return "Player"