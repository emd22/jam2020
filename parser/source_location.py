class SourceLocation:
    def __init__(self, filename, col=1, row=1):
        self.filename = filename
        self.col = col
        self.row = row

    @property
    def col_row(self):
        return (self.col, self.row)
  