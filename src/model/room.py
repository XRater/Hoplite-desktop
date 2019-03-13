class Room(object):
    def __init__(self, height, width, corner_row, corner_column):
        self.height = height
        self.width = width
        self.corner_row = corner_row
        self.corner_column = corner_column

    def contains_cell(self, cell):
        """

        :param cell: a cell to check
        :return: true if room contains cell
        """
        return (cell.row >= self.corner_row and cell.column >= self.corner_column) and \
               (cell.row < self.corner_row + self.height and cell.column < self.corner_column + self.width)
