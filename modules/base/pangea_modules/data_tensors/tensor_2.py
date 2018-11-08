
class Tensor2:
    """Represent a group of groups of atomic data."""
    pass


class VectorGroup(Tensor2):

    def __init__(self, **vectors):
        self.vectors = vectors

    def __get__(self, key):
        return self.vectors[key]


class Matrix(Tensor2):

    def __init__(self, data, row_indexed=True, col_indexed=True):
        self.data = data
        self.row_indexed, self.col_indexed = row_indexed, col_indexed

    def __get__(self, key):
        return self.data[key]
