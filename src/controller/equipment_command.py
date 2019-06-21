from src.controller.command import Command


class EquipmentCommand(Command):
    """A command for wearing an item from inventory."""

    def __init__(self, item, player_id):
        self.item = item
        self.player_id = player_id

    def execute(self, logic):
        logic.equip_item(self.player_id, self.item)
