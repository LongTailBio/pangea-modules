"""Represent models 2 steps from atomic."""
from pangea_modules.base.data_tensor import Vector, Matrix

from .models import UnlimitedGroupModel
from .tensor_0 import Tensor0Model
from .tensor_1 import VectorModel
from .utils import flip_nested_dict


class Tensor2Model:  # pylint: disable=too-few-public-methods
    """Represent a data model that groups groups of atomic data."""
    pass


class MatrixModel(UnlimitedGroupModel, Tensor2Model):  # pylint: disable=too-few-public-methods
    """Represent a mathematical matrix to the db."""

    def __init__(self, dtype: Tensor0Model, row_indexed=True, col_indexed=True):
        super(MatrixModel).__init__(
            self,
            VectorModel(dtype, indexed=row_indexed),
            indexed=col_indexed,
            return_type=Matrix,
        )

    def promote(self, observations): # pylint: disable=no-self-use
        """Return a dictionary of matrices, one matrix for column."""
        flipped = flip_nested_dict(observations, recurse=True)
        promoted = {}
        for col_name, outer_dict in flipped.items():
            inner_matrix = {}
            for row_name, inner_dict in outer_dict.items():
                inner_matrix[row_name] = Vector(inner_dict)
            promoted[col_name] = Matrix(inner_matrix)
        return promoted
