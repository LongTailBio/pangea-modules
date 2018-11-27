"""Represent level 2 tensors."""

import pandas as pd

from .matrix_data_processing import MatrixProcessing
from .tensor_1 import Vector


class Tensor2:  # pylint: disable=too-few-public-methods
    """Represent a group of groups of atomic data."""

    dimensions = 2


class VectorGroup(Tensor2):  # pylint: disable=too-few-public-methods
    """Represent a discrete, limited, group of named vectors."""

    def __init__(self, **vectors):
        self.vectors = vectors

    def __getitem__(self, key):
        return self.vectors[key]


class Matrix(MatrixProcessing, Tensor2):
    """Represent an unlimited group of vectors."""

    def __init__(self, data):
        if not isinstance(data, pd.DataFrame):
            data = pd.DataFrame(data)
        super().__init__(data, change_types={pd.Series: Vector})

    def __new__(cls, data, *args, **kwargs):
        """Overwrite new so that special methods will receive the correct types."""
        if not isinstance(data, pd.DataFrame):
            data = pd.DataFrame.from_dict(data, orient='columns')
        return MatrixProcessing.__new__(cls, data, *args, **kwargs)
