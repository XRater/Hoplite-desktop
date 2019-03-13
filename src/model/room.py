class Room(object):
    def __init__(self, height, width, corner_row, corner_column):
        self.height = height
        self.width = width
        self.corner_row = corner_row
        self.corner_column = corner_column

    def get_common_range(self, other):
        common_range = self.get_common_range_(other)
        if common_range is None:
            common_range = other.get_common_range_(self)
        return common_range

    def get_common_range_(self, other):
        if self.corner_row + 1 + self.height == other.corner_row:
            column_range = self.get_column_range()
            other_column_range = other.get_column_range()
            lower = max(column_range[0], other_column_range[0])
            upper = min(column_range[1], other_column_range[1])
            if lower <= upper:
                return 'column', self.corner_row + self.height, lower, upper

        if self.corner_column + 1 + self.width == other.corner_column:
            row_range = self.get_row_range()
            other_row_range = other.get_row_range()
            lower = max(row_range[0], other_row_range[0])
            upper = min(row_range[1], other_row_range[1])
            if lower <= upper:
                return 'row', self.corner_column + self.width, lower, upper

        return None

    def get_row_range(self):
        return self.corner_row, self.corner_row + self.height - 1

    def get_column_range(self):
        return self.corner_column, self.corner_column + self.width - 1

    def contains_cell(self, cell):
        """

        :param cell: a cell to check
        :return: true if room contains cell
        """
        return (cell.row >= self.corner_row and cell.column >= self.corner_column) and \
               (cell.row < self.corner_row + self.height and cell.column < self.corner_column + self.width)
