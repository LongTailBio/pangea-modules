"""Represent tensors that contain atomic tensors."""

import numpy as np

from .vector_data_access import VectorAccess


class Tensor1:  # pylint: disable=too-few-public-methods
    """Represent a group of atomic data."""

    dimensions = 1


class ScalarGroup(Tensor1):  # pylint: disable=too-few-public-methods
    """Represent a tensor that contains a limited predefined set of atomics."""

    def __init__(self, **scalars):
        self.scalars = scalars

    def __getitem__(self, key):
        return self.scalars[key]


class Vector(VectorAccess, Tensor1):
    """Represent a sequence of numerical scalars."""

    def as_compositional(self):
        """Return a vector proportional to this one that sums to 1."""
        my_sum = self.sum()
        return self.operate(lambda val: val / my_sum)

    def percentile(self, *percentiles):
        """Return a vector of percentiles of the data."""
        return type(self)(np.percentile(self.values, percentiles))  # pylint: disable=no-member

    def quartiles(self):
        """Return a Vector of length 5 for 0, 25, 50, 75, 100 percentiles."""
        return self.percentile(0, 25, 50, 75, 100)

    def num_non_zero(self, zero_thresh=0.00000000001):
        """Return the number of elements with value larger than <zero_thresh>."""
        vals = [val for _, val in self.items() if abs(val) < zero_thresh]
        return len(vals)
