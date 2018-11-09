"""Represent tensors that contain atomics."""
from pangea_modules.base.data_tensors import Vector, Matrix

from .models import UnlimitedGroupModel
from .tensor_0 import ScalarModel


class Tensor1Model:  # pylint: disable=too-few-public-methods
    """Represent a data model that groups atomic data."""
    pass


class VectorModel(UnlimitedGroupModel, Tensor1Model):  # pylint: disable=too-few-public-methods
    """Represent a mathematical vector for the db."""

    def __init__(self, dtype: ScalarModel, indexed=True):
        super(dtype)
        self.dtype = dtype
        self.indexed = indexed
        self.return_type = Vector

    def promote(self, observations):
        """Return a matrix"""
        matrix = Matrix(observations)
        return matrix.transposed()
