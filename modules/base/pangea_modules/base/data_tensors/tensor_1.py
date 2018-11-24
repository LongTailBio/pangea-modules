"""Represent tensors that contain atomic tensors."""

import pandas as pd

from .vector_data_processing import VectorProcessing


class Tensor1:  # pylint: disable=too-few-public-methods
    """Represent a group of atomic data."""

    dimensions = 1


class ScalarGroup(Tensor1):  # pylint: disable=too-few-public-methods
    """Represent a tensor that contains a limited predefined set of atomics."""

    def __init__(self, **scalars):
        self.scalars = scalars

    def __getitem__(self, key):
        return self.scalars[key]


class Vector(VectorProcessing, Tensor1):
    """Represent a sequence of numerical scalars."""

    def __init__(self, data):
        if not isinstance(data, pd.Series):
            data = pd.Series(data)
        super().__init__(data)
        self.data = self._obj

    def __new__(cls, data, *args, **kwargs):
        if not isinstance(data, pd.Series):
            data = pd.Series(data)
        return VectorProcessing.__new__(cls, data, *args, **kwargs)
