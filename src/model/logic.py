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
        if self.isWall(new_row, new_column):
            logging.info('Player could not move to position {row} {column} because of wall'.format(
                row=new_row,
                column=new_column
            ))
            return False
        player.cell = self._dungeon.field.cells[new_row][new_column]
        logging.info('Player moved to position {row} {column}'.format(row=new_row, column=new_column))
        return True

    def isWall(self, row, column):
        return self._dungeon.field.cells[row][column].cell_type == CellType.WALL

    def make_turn(self):
        print("Turn")
        pass
