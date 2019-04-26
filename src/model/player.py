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

    def have_space_in_inventory(self):
        return len(self.inventory) < self.INVENTORY_SIZE

    def is_alive(self):
        return self.health > 0

    def collect_loot(self, item):
        """
        Adds item to inventory if it isn't full or throws raises InventoryFullException otherwise
        :param item: loot of type GameObject
        :return: noting
        """
        if len(self.inventory) < self.INVENTORY_SIZE:
            self.inventory.append(item)
            return
        raise InventoryFullException()

    def wear_equipment(self, index):
        """
        Wears equipment and returns currently wore equipment of the same body part back to the inventory, if it exists
        If inventory doesn't contain equipment with given index raises NoEquipmentException
        :param index: index
        :return: nothing
        """
        equipment = self.inventory[index]
        if index >= len(self.inventory) or not isinstance(equipment, Equipment):
            raise NoEquipmentException()
        currently_wore = self.equipment[equipment.equipment_type] \
            if equipment.equipment_type in self.equipment else None
        self.equipment[equipment.equipment_type] = equipment
        if currently_wore is None:
            self.inventory = self.inventory[:index] + self.inventory[index + 1:]
        else:
            self.inventory[index] = currently_wore

    def __str__(self):
        return "Player"


class InventoryFullException(Exception):
    """
    Error shell class
    """
    pass


class NoEquipmentException(Exception):
    """
    Error shell class
    """
    pass
