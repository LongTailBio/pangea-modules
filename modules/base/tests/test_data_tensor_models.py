"""Test suite for Data Tensor Models."""
from unittest import TestCase

import mongoengine as mdb

from pangea_modules.base.data_tensors import (
    Vector,
    Matrix,
)
from pangea_modules.base.data_tensor_models import (
    VectorModel,
    MatrixModel,
)


class TestDataTensorModels(TestCase):
    """Test suite for Data Tensor Models."""

    def test_indexed_vector_produces_correct_schema(self):
        """Ensure an indexed vector produces the correct mongoengine type."""
        indexed_vector_model = VectorModel(float, indexed=True)
        self.assertIs(type(indexed_vector_model.get_document_class()), mdb.MapField)

    def test_unindexed_vector_produces_correct_schema(self):
        """Ensure an unindexed vector produces the correct mongoengine type."""
        unindexed_vector_model = VectorModel(int, indexed=False)
        self.assertIs(type(unindexed_vector_model.get_document_class()), mdb.ListField)

    def test_indexed_vector_from_son(self):
        """Ensure an indexed vector builds the correct type from a SON blob."""
        indexed_vector_model = VectorModel(float, indexed=True)
        indexed_vector = indexed_vector_model.from_son({'a': 1, 'b': 2})
        self.assertIs(type(indexed_vector), Vector)

    def test_unindexed_vector_from_son(self):
        """Ensure an indexed vector builds the correct type from a SON blob."""
        unindexed_vector_model = VectorModel(float, indexed=False)
        unindexed_vector = unindexed_vector_model.from_son([1, 2])
        self.assertIs(type(unindexed_vector), Vector)

    def test_indexed_matrix_produces_correct_schema(self):
        """Ensure an indexed matrix produces the correct mongoengine type."""
        indexed_matrix_model = MatrixModel(float, col_indexed=True)
        self.assertIs(type(indexed_matrix_model.get_document_class()), mdb.MapField)

    def test_indexed_matrix_from_son(self):
        """Ensure an indexed matrix builds the correct type from a SON blob."""
        data = {
            'col_1': {'row_1': 1, 'row_2': 2},
            'col_2': {'row_1': 3, 'row_2': 4},
        }
        indexed_matrix_model = MatrixModel(float, col_indexed=True)
        indexed_matrix = indexed_matrix_model.from_son(data)
        self.assertIs(type(indexed_matrix), Matrix)
        self.assertTrue(indexed_matrix.col_indexed)
        self.assertTrue(indexed_matrix.row_indexed)
