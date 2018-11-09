"""Represent tensors that contain atomics."""
from pangea_modules.base.data_tensor import Vector, Matrix

from .models import DataModel, UnlimitedGroupModel
from .tensor_0 import ScalarModel


class Tensor1Model:  # pylint: disable=too-few-public-methods
    """Represent a data model that groups atomic data."""
    pass


class VectorModel(UnlimitedGroupModel, Tensor1Model):
    """Represent a mathematical vector for the db."""

    def __init__(self, dtype: ScalarModel, indexed=True):
        super(VectorModel).__init__(self, dtype, indexed=indexed, return_type=Vector)
        self.dtype = dtype
        self.indexed = indexed

    def promote(self, observations):
        """Return a matrix"""
        if observations.isinstance(dict):
            matrix = Matrix(observations, row_indexed=self.indexed, col_indexed=True)
        else:
            matrix = Matrix(observations, row_indexed=self.indexed, col_indexed=False)
        return matrix.transpose()
