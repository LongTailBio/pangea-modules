
import pandas as pd


class Tensor1:
    """Represent a group of atomic data."""
    pass


class ScalarGroup(Tensor1):

    def __init__(self, **scalars):
        self.scalars = scalars

    def __get__(self, key):
        return self.scalars[key]


class Vector(Tensor1):

    def __init__(self, data):
        self.data = data
        if type(self.data) is list:
            self.data = {ind: val for ind, val in enumerate(data)}

    def __get__(self, key):
        return self.data[key]

    def __len__(self):
        """Return the length of this vector."""
        return len(self.data)

    def as_pandas(self):
        """Return a pandas series based on this vector."""
        return pd.Series.from_dict(self.data)

    def iter(self):
        """Yield tuples of key, value."""
        for key, val in self.data.items():
            yield key, val

    def sum(self):
        """Return the sum of values in this vector."""
        return sum(self.data.values())

    def mean(self):
        """Return the mean value of this vector."""
        return self.sum() / len(self)

    def median(self):
        """Return the median value of this vector."""
        vals = list(self.data.values())
        vals = sorted(vals)
        if len(vals) % 2 == 0:
            ind = len(vals) / 2
            return (vals[ind] + vals[ind - 1]) / 2
        return vals[len(vals) // 2]

    def as_compositional(self):
        """Return a vector proportional to this one that sums to 1."""
        my_sum = self.sum()
        return Vector({key: val / my_sum for key, val in self.data.items()}, indexed=self.indexed)
