"""Represent tensors that contain atomic tensors."""

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
        self.data = data
        if isinstance(data, list):
            self.data = {indvar: val for indvar, val in enumerate(data)}
