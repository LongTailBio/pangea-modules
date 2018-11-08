"""Test suite for Data Tensor Models."""

import mongoengine as mdb
from unittest import TestCase

from pangea_modules.base.data_tensors import (
    Vector,
)
from pangea_modules.base.data_tensor_models import (
    VectorModel,
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
        self.assertTrue(indexed_vector.indexed)

    def test_unindexed_vector_from_son(self):
        """Ensure an indexed vector builds the correct type from a SON blob."""
        unindexed_vector_model = VectorModel(float, indexed=False)
        unindexed_vector = unindexed_vector_model.from_son([1, 2])
        self.assertIs(type(unindexed_vector), Vector)
        self.assertFalse(unindexed_vector.indexed)
