"""Represent tensors that contain atomic tensors."""

import pandas as pd

from .vector_data_processing import VectorProcessing
from .proxy import Proxy


class Tensor1:  # pylint: disable=too-few-public-methods
    """Represent a group of atomic data."""

    dimensions = 1


class ScalarGroup(Tensor1):  # pylint: disable=too-few-public-methods
    """Represent a tensor that contains a limited predefined set of atomics."""

    def __init__(self, **scalars):
        self.scalars = scalars

    def __getitem__(self, key):
        return self.scalars[key]


class Vector(Proxy, Tensor1):
    """Represent a sequence of numerical scalars."""

    def __init__(self, data):
        super().__init__(data)
        self.data = data

    def to_pandas(self):
        """Return a pandas series based on this vector."""
        return self.data

    def operate(self, operator):
        """Return a vector with <operator> applied to each element."""
        return type(self)({key: operator(val) for key, val in self.items()})

    def reduce(self, operator):
        """Return the function applied to the values in the vector.

        Order of values is not guaranteed.
        """
        return operator(self.get_values())

    @classmethod
    def from_list(cls, data):
        data = pd.Series(data)
        return cls(data)
