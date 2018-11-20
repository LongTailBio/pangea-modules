"""Represent tensors that contain atomic tensors."""
import pandas as pd
import numpy as np

class Tensor1:  # pylint: disable=too-few-public-methods
    """Represent a group of atomic data."""
    pass


class ScalarGroup(Tensor1):  # pylint: disable=too-few-public-methods
    """Represent a tensor that contains a limited predefined set of atomics."""
    def __init__(self, **scalars):
        self.scalars = scalars

    def __getitem__(self, key):
        return self.scalars[key]


class Vector(Tensor1):
    """Represent a sequence of numerical scalars."""

    def __init__(self, data):
        self.data = data
        if isinstance(data, list):
            self.data = {indvar: val for indvar, val in enumerate(data)}

    def __getitem__(self, key):
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
            ind = len(vals) // 2
            return (vals[ind] + vals[ind - 1]) / 2
        return vals[len(vals) // 2]

    def as_compositional(self):
        """Return a vector proportional to this one that sums to 1."""
        my_sum = self.sum()
        return Vector({key: val / my_sum for key, val in self.data.items()})

    def percentile(self, *percentiles):
        """Return a vector of percentiles of the data."""
        return Vector(np.percentile(list(self.data.values()), percentiles))

    def quartiles(self):
        """Return a Vector of length 5 for 0, 25, 50, 75, 100 percentiles."""
        return self.percentile(0, 25, 50, 75, 100)

    def num_non_zero(self, zero_thresh=0.00000000001):
        """Return the number of elements with value larger than <zero_thresh>."""
        vals = [val for _, val in self.iter() if abs(val) < zero_thresh]
        return len(vals)
