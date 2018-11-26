"""Test suite for Data Tensors."""

from unittest import TestCase

from pangea_modules.base.data_tensors import (
    Vector,
    Matrix,
)


class TestDataTensors(TestCase):
    """Test suite for Data Tensors."""

    def test_indexed_vector_data_retrieval(self):
        """Ensure an indexed vector retrieves data correctly."""
        data = {'a': 1, 'b': 2}
        indexed_vector = Vector(data)
        for key, val in data.items():
            self.assertEqual(indexed_vector[key], val)

    def test_unindexed_vector_data_retrieval(self):
        """Ensure an unindexed vector retrieves data correctly."""
        data = [1, 2]
        unindexed_vector = Vector(data)
        for key, val in enumerate(data):
            self.assertEqual(unindexed_vector[key], val)

    def test_vector_len(self):
        """Check that the length is correct."""
        data = [1, 2, 3, 4, 5]
        vec = Vector(data)
        self.assertEqual(len(vec), len(data))

    def test_vector_mult(self):
        """Check that the length is correct."""
        data = [1, 2, 3, 4, 5]
        multiplied = 2 * Vector(data)
        for i, val in enumerate(data):
            self.assertEqual(2 * val, multiplied[i])

    def test_vector_add(self):
        """Check that the length is correct."""
        data = [1, 2, 3, 4, 5]
        multiplied = 2 + Vector(data)
        for i, val in enumerate(data):
            self.assertEqual(2 + val, multiplied[i])

    def test_vector_sum(self):
        """Check that the sum is correct."""
        data = [1, 2, 3, 4, 5]
        vec = Vector(data)
        self.assertEqual(vec.sum(), sum(data))

    def test_vector_mean(self):
        """Check that the mean is returned."""
        data = [1, 2, 3, 4, 5]
        vec = Vector(data)
        self.assertEqual(3, vec.mean())

    def test_vector_median(self):
        """Check that the mean is returned."""
        data = [1, 2, 3, 4, 5]
        vec = Vector(data)
        self.assertEqual(3, vec.median())

        data = [3, 1, 2, 4]
        vec = Vector(data)
        self.assertEqual(2.5, vec.median())

    def test_matrix_dimensions(self):
        """Check that we get the proper dimensions."""
        matrix = Matrix(
            {
                'a': Vector([1, 2, 3]),
                'b': Vector([4, 5, 6]),
            }
        )
        self.assertEqual(matrix.ncols(), 2)
        self.assertEqual(matrix.nrows(), 3)
        self.assertEqual(matrix.shape, (3, 2))

    def test_matrix_col_means(self):
        """Check that we get the proper col means."""
        matrix = Matrix(
            {
                'a': Vector([1, 2, 3]),
                'b': Vector([4, 5, 6]),
            }
        )
        col_means = matrix.col_means()
        self.assertIsInstance(col_means, Vector)
        self.assertEqual(col_means['a'], 2)
        self.assertEqual(col_means['b'], 5)

    def test_matrix_transpose(self):
        """Check that matrix transposition works."""
        matrix = Matrix(
            {
                'a': Vector([1, 2, 3]),
                'b': Vector([4, 5, 6]),
            }
        )
        transposed = matrix.transposed()
        self.assertIsInstance(transposed, Matrix)
        self.assertEqual(transposed.ncols(), matrix.nrows())
        self.assertEqual(transposed.nrows(), matrix.ncols())

    def test_matrix_tsne_returns_data(self):
        """Test that TSNE returns data in the proper form."""
        matrix = Matrix(
            {
                'a': Vector([1, 2, 3]),
                'b': Vector([4, 5, 6]),
                'c': Vector([7, 8, 9]),
                'd': Vector([3, 2, 1]),
            }
        )
        tsne_out = matrix.tsne()
        self.assertIsInstance(tsne_out, Matrix)
        self.assertEqual((3, 2), tsne_out.shape)
