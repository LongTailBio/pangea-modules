
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

    def __init__(self, data, indexed=True):
        self.data = data
        self.indexed = indexed

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
        if self.indexed:
            for key, val in self.data:
                yield key, val
        else:
            for ind, val in enumerate(self.data):
                yield ind, val

    def sum(self):
        """Return the sum of values in this vector."""
        if self.indexed:
            return sum(self.data.values())
        return sum(self.data)

    def mean(self):
        """Return the mean value of this vector."""
        return self.sum() / len(self)

    def median(self):
        """Return the median value of this vector."""
        vals = self.data
        if self.indexed:
            vals = list(self.data.values())
        vals = sorted(vals)
        if len(vals) % 2 == 0:
            ind = len(vals) / 2
            return (vals[ind] + vals[ind - 1]) / 2
        return vals[len(vals) // 2]

    def as_compositional(self):
        """Return a vector proportional to this one that sums to 1."""
        my_sum = self.sum()
        if self.indexed:
            return Vector({key: val / my_sum for key, val in self.data.items()}, indexed=True)
        return Vector([val / my_sum for val in self.data], indexed=False)
