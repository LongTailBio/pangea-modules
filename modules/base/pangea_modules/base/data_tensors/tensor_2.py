"""Represent level 2 tensors."""

from .matrix_data_processing import MatrixProcessing


class Tensor2:  # pylint: disable=too-few-public-methods
    """Represent a group of groups of atomic data."""
    pass


class VectorGroup(Tensor2):  # pylint: disable=too-few-public-methods
    """Represent a discrete, limited, group of named vectors."""

    def __init__(self, **vectors):
        self.vectors = vectors

    def __getitem__(self, key):
        return self.vectors[key]


class Matrix(MatrixProcessing, Tensor2):
    """Represent an unlimited group of vectors."""

    def __init__(self, data):
        self.data = data
        if isinstance(data, list):
            self.data = {ind: val for ind, val in enumerate(data)}
