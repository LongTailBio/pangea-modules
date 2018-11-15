"""Represent tensors that contain atomics."""

from pangea_modules.base.data_tensors import Vector, Matrix

from .models import UnlimitedGroupModel
from .tensor_0 import ScalarModel


class Tensor1Model:  # pylint: disable=too-few-public-methods
    """Represent a data model that groups atomic data."""
    pass


class VectorModel(UnlimitedGroupModel, Tensor1Model):  # pylint: disable=too-few-public-methods
    """Represent a mathematical vector for the db."""

    def __init__(self, dtype: ScalarModel, indexed=True, allowed_keys=None):
        super().__init__(dtype, indexed=indexed, return_type=Vector, allowed_keys=allowed_keys)
        if self.dtype in (float, int):
            self.dtype = ScalarModel(dtype=self.dtype)

    def promote(self, observations):
        """Return a matrix"""
        matrix = Matrix(observations)
        return matrix.transposed()
