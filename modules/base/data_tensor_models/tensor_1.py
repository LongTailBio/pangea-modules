
from data_tensor import Vector

from .models import DataModel, UnlimitedGroupModel
from .tensor_0 import ScalarModel


class Tensor1Model:
    """Represent a data model that groups atomic data."""
    pass


class VectorModel(UnlimitedGroupModel, Tensor1Model):
    """Represent a mathematical vector for the db."""

    def __init__(self, dtype: ScalarModel, indexed=True):
        super(Vector).__init__(self, dtype, indexed=indexed, return_type=Vector)
        self.dtype = dtype
        self.indexed = indexed
