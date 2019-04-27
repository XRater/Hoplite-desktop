from src.controller.command import Command


class EquipmentCommand(Command):
    """A command for wearing an item from inventory."""

    def __init__(self, item):
        self.item = item

    def execute(self, logic):
        logic.equip_item(self.item)
