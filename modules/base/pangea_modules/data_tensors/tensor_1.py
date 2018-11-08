

class Tensor1:
    """Represent a group of atomic data."""
    pass


class ScalarGroup(Tensor1):

    def __init__(self, **scalars):
        self.scalars = scalars

    def __get__(self, key):
        return self.scalars[key]


class Vector(Tensor1):

    def __init__(self, data, indexed=True):
        self.data = data
        self.indexed = indexed

    def __get__(self, key):
        return self.data[key]
