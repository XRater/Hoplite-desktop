from src.controller.command import Command
from src.controller.direction import Direction


class MoveCommand(Command):
    """A command for moving player."""

    def __init__(self, direction):
        self.direction = direction

    def execute(self, logic):
        if self.direction == Direction.DOWN:
            return logic.move_player(1, 0)
        elif self.direction == Direction.UP:
            return logic.move_player(-1, 0)
        elif self.direction == Direction.LEFT:
            return logic.move_player(0, -1)
        elif self.direction == Direction.RIGHT:
            return logic.move_player(0, 1)
