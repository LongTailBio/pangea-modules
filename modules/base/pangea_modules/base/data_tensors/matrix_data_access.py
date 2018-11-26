"""Handle data access fucntionality for matrix class."""

import pandas as pd

from .tensor_1 import Vector
from .proxy import Proxy


class MatrixAccess(Proxy):
    """Handle all data access fucntions for Matrix class."""

    def __init__(self, data):
        super().__init__(data)
        self.data = data

    def ncols(self):
        """Return the number of columns in this matrix."""
        return self.shape[1]

    def nrows(self):
        """Return the number of rows in this matrix."""
        return self.shape[0]

    def colnames(self):
        """Return a lsit of colnames."""
        return self.columns

    def rownames(self):
        """Return a list of rownames."""
        return self.index

    def to_pandas(self):
        """Return this matrix as a pandas dataframe."""
        return self.data

    def to_numpy(self):
        """Return this matrix as a numpy matrix."""
        return self.values

    def iter_cols(self, operator=lambda x: x):
        """Yield tuples of key, vectors one for each col."""
        for key, col in self.iteritems():
            yield key, operator(col)

    def iter_rows(self, operator=lambda x: x):
        """Yield key, vector pairs for each row. Ineffecient."""
        for key, row in self.iterrows():
            yield key, operator(row)

    def operate_cols(self, operator):
        """Return a dict with operator applied to each column."""
        return dict(self.iter_cols(operator=operator))

    def operate_rows(self, operator):
        """Return a dict with operator applied to each row."""
        return dict(self.iter_rows(operator=operator))

    def reduce_cols(self, operator):
        """Return a Vector with operator applied to each column."""
        return Vector(self.operate_cols(operator))

    def reduce_rows(self, operator):
        """Return a Vector with operator applied to each row."""
        return Vector(self.operate_rows(operator))

    def apply_cols(self, operator):
        """Return a Matrix with operator applied to each column."""
        return self.apply(operator, axis=1)

    def apply_rows(self, operator):
        """Return a Matrix with operator applied to each row."""
        return self.apply(operator, axis=0)

    def filter_cols(self, test):
        """Return a matrix with only columns where `test` returns True.

        As input `test` is given a tuple of <column_name>, <vector>.
        """
        kept = {
            col_name: col_vals
            for col_name, col_vals in self.iter_cols()
            if test(col_name, col_vals)
        }
        return type(self)(kept)

    def filter_rows(self, test):
        """Return a matrix with only columns where `test` returns True.

        As input `test` is given a tuple of <column_name>, <vector>.
        """
        kept = {
            col_name: col_vals
            for col_name, col_vals in self.transposed().iter_cols()
            if test(col_name, col_vals)
        }
        return type(self)(kept).transposed()

    def transposed(self):
        """Flip rows and columns of this matrix."""
        return self.T








