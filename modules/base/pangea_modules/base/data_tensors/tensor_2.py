"""Represent level 2 tensors."""
import pandas as pd

from .tensor_1 import Vector


class Tensor2:  # pylint: disable=too-few-public-methods
    """Represent a group of groups of atomic data."""
    pass


class VectorGroup(Tensor2):  # pylint: disable=too-few-public-methods
    """Represent a discrete, limited, group of named vectors."""

    def __init__(self, **vectors):
        self.vectors = vectors

    def __getitem__(self, key):
        return self.vectors[key]


class Matrix(Tensor2):
    """Represent an unlimited group of vectors."""

    def __init__(self, data):
        self.data = data
        if isinstance(data, list):
            self.data = {ind: val for ind, val in enumerate(data)}

    def __getitem__(self, key):
        return self.data[key]

    def ncols(self):
        """Return the number of columns in this matrix."""
        return len(self.data)

    def nrows(self):
        """Return the number of rows in this matrix."""
        if not self.ncols():
            return 0
        val = len(next(iter(self.data.values())))
        if val:
            return val
        return 0

    def as_pandas(self):
        """Return this matrix as a pandas dataframe."""
        return pd.DataFrame.from_dict(self.data)

    def iter_cols(self, operator=lambda x: x):
        """Yield tuples of key, vectors one for each col."""
        for key, col in self.data.items():
            yield key, operator(col)

    def operate_cols(self, operator):
        """Return a dict with operator applied to each column."""
        return dict(self.iter_cols(operator=operator))

    def reduce_cols(self, operator):
        """Return a Vector with operator applied to each column."""
        return Vector(self.operate_cols(operator))

    def apply_cols(self, operator):
        """Return a Matrix with operator applied to each column."""
        return Matrix(self.operate_cols(operator))

    def filter_cols(self, test):
        """Return a matrix with only columns where `test` returns True.

        As input `test` is given a tuple of <column_name>, <vector>.
        """
        kept = {
            col_name: col_vals
            for col_name, col_vals in self.iter_cols()
            if test(col_name, col_vals)
        }
        return Matrix(kept)

    def transposed(self):
        """Flip rows and columns of this matrix."""
        outer = {}
        for col_name, row in self.data.items():
            for row_name, val in row.iter():
                try:
                    outer[row_name][col_name] = val
                except KeyError:
                    outer[row_name] = {col_name: val}
        outer = {row_name: Vector(row) for row_name, row in outer.items()}
        return Matrix(outer)

    def iter_rows(self, operator=lambda x: x):
        """Yield key, vector pairs for each row. Ineffecient."""
        return self.transposed().iter_cols(operator=operator)

    def operate_rows(self, operator):
        """Return a dict with operator applied to each row."""
        return dict(self.iter_cols(operator=operator))

    def reduce_rows(self, operator):
        """Return a Vector with operator applied to each row."""
        return Vector(self.operate_rows(operator))

    def apply_rows(self, operator):
        """Return a Matrix with operator applied to each row."""
        return Matrix(self.operate_rows(operator)).transposed()

    def filter_rows(self, test):
        """Return a matrix with only columns where `test` returns True.

        As input `test` is given a tuple of <column_name>, <vector>.
        """
        kept = {
            col_name: col_vals
            for col_name, col_vals in self.transposed().iter_cols()
            if test(col_name, col_vals)
        }
        return Matrix(kept).transposed()

    def col_means(self):
        """Return a vector with the means of each column."""
        return self.operate_cols(lambda col: col.mean())

    def row_means(self):
        """Return a vector with means for each row."""
        return self.transposed().col_means()

    def compositional_rows(self):
        """Return a Matrix where each row sums to 1."""
        return self.apply_rows(lambda row: row.as_compositional())
