import logging

from src.model.cell import CellType, CellVision


class Logic(object):
    def __init__(self, dungeon):
        self._dungeon = dungeon
        self._init_dungeon()

    def _init_dungeon(self):
        player = self._dungeon.player
        player_room = self._dungeon.field.get_room_for_cell(player.cell)
        self.set_vision_for_room(player_room, CellVision.VISIBLE)

    # Moves player to the new cell if possible
    # Returns true if player was moved and false otherwise
    def move_player(self, delta_row, delta_column):
        player = self._dungeon.player
        new_row = player.cell.row + delta_row
        new_column = player.cell.column + delta_column
        logging.info(delta_column)
        logging.info(delta_row)
        if not (self.can_move_to(new_row, new_column)):
            logging.info('Player could not move to position {row} {column} because of wall'.format(
                row=new_row,
                column=new_column
            ))
            return False
        room = self._dungeon.field.get_room_for_cell(player.cell)
        player.cell = self._dungeon.field.cells[new_row][new_column]
        new_room = self._dungeon.field.get_room_for_cell(player.cell)
        if room != new_room:
            if room is not None:
                logging.info("Player stepped out of the room {row} {column}".format(
                    row=room.corner_row,
                    column=room.corner_column
                ))
                self.set_vision_for_room(room, CellVision.FOGGED)
            if new_room is not None:
                logging.info("Player stepped into room {row} {column}".format(
                    row=new_room.corner_row,
                    column=new_room.corner_column
                ))
                self.set_vision_for_room(new_room, CellVision.VISIBLE)
        logging.info('Player moved to position {row} {column}'.format(row=new_row, column=new_column))
        return True

    # Checks if player can move to th target row and column
    def can_move_to(self, row, column):
        return self.in_dungeon(row, column) and self._dungeon.field.cells[row][column].cell_type != CellType.WALL

    def in_dungeon(self, row, column):
        return not (row < 0 or column < 0 or row >= self._dungeon.field.height or column >= self._dungeon.field.width)

    # Sets vision for every cell in room
    def set_vision_for_room(self, room, vision):
        for row in range(room.corner_row - 1, room.corner_row + room.height + 1):
            for column in range(room.corner_column - 1, room.corner_column + room.width + 1):
                if self.in_dungeon(row, column):
                    self._dungeon.field.cells[row][column].vision = vision

    def make_turn(self):
        print("Turn")
        pass
