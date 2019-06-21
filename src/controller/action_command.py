from src.controller.action import Action
from src.controller.command import Command


class ActionCommand(Command):
    """A command for moving player."""

    def __init__(self, action):
        self.action = action

    def execute(self, logic):
        if self.action == Action.DOWN:
            return logic.move_player(1, 0)
        elif self.action == Action.UP:
            return logic.move_player(-1, 0)
        elif self.action == Action.LEFT:
            return logic.move_player(0, -1)
        elif self.action == Action.RIGHT:
            return logic.move_player(0, 1)
