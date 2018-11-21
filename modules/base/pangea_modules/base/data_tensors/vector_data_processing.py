"""Data processing fucntionality for a vector."""

import numpy as np

from .vector_data_access import VectorAccess


class VectorProcessing(VectorAccess):  # pylint: disable=no-member
    """Represent a sequence of numerical scalars."""

    def sum(self):
        """Return the sum of values in this vector."""
        return self.reduce(sum)

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
        return self.operate(lambda val: val / my_sum)

    def percentile(self, *percentiles):
        """Return a vector of percentiles of the data."""
        return type(self)(np.percentile(list(self.data.values()), percentiles))

    def quartiles(self):
        """Return a Vector of length 5 for 0, 25, 50, 75, 100 percentiles."""
        return self.percentile(0, 25, 50, 75, 100)

    def num_non_zero(self, zero_thresh=0.00000000001):
        """Return the number of elements with value larger than <zero_thresh>."""
        vals = [val for _, val in self.iter() if abs(val) < zero_thresh]
        return len(vals)
