import logging

from src.model.cell import CellType


class Logic(object):
    def __init__(self, dungeon):
        self._dungeon = dungeon

    def move_player(self, delta_row, delta_column):
        player = self._dungeon.player
        new_row = player.cell.row + delta_row
        new_column = player.cell.column + delta_column
        logging.info(delta_column)
        logging.info(delta_row)
        if not(self.can_move_to(new_row, new_column)):
            logging.info('Player could not move to position {row} {column} because of wall'.format(
                row=new_row,
                column=new_column
            ))
            return False
        player.cell = self._dungeon.field.cells[new_row][new_column]
        logging.info('Player moved to position {row} {column}'.format(row=new_row, column=new_column))
        return True

    def can_move_to(self, row, column):
        if row < 0 or column < 0 or row >= self._dungeon.field.height or column >= self._dungeon.field.width:
            return False
        return self._dungeon.field.cells[row][column].cell_type != CellType.WALL

    def make_turn(self):
        print("Turn")
        pass
