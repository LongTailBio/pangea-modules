"""Test suite for Data Tensors."""

from unittest import TestCase

from pangea_modules.base.data_tensors import (
    ScalarGroup,
    Vector,
)


class TestDataTensors(TestCase):
    """Test suite for Data Tensors."""

    def test_scalar_group_retrieval(self):
        """Ensure scalar group retrieval works correctly."""
        data = {'a': 1, 'b': 2}
        scalar_group = ScalarGroup(**data)
        for key, val in data.items():
            self.assertEquals(scalar_group[key], val)

    def test_indexed_vector_data_retrieval(self):
        """Ensure an indexed vector retrieves data correctly."""
        data = {'a': 1, 'b': 2}
        indexed_vector = Vector(data, indexed=True)
        for key, val in data.items():
            self.assertEquals(indexed_vector[key], val)

    def test_unindexed_vector_data_retrieval(self):
        """Ensure an unindexed vector retrieves data correctly."""
        data = [1, 2]
        unindexed_vector = Vector(data, indexed=False)
        for key, val in enumerate(data):
            self.assertEquals(unindexed_vector[key], val)
