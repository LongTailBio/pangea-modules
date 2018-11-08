
from data_tensor import Matrix

from .models import UnlimitedGroupModel
from .tensor_0 import Tensor0Model
from .tensor_1 import VectorModel


class Tensor2Model:
    """Represent a data model that groups groups of atomic data."""
    pass


class MatrixModel(UnlimitedGroupModel, Tensor2Model):
    """Represent a mathematical matrix to the db."""

    def __init__(self, dtype: Tensor0Model, row_indexed=True, col_indexed=True):
        super(MatrixModel).__init__(
            self,
            VectorModel(dtype, indexed=row_indexed),
            indexed=col_indexed,
            return_type=Matrix,
        )
