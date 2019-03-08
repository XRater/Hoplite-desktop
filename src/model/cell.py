class Cell(object):
    def __init__(self, row, column, parent):
        self.row = row
        self.column = column
        self._parent = parent
