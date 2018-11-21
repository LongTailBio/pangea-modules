"""Handle data access fucntionality for matrix class."""

import pandas as pd

from .tensor_1 import Vector


class MatrixAccess:
    """Handle all data access fucntions for Matrix class."""

    data = {}

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

    def shape(self):
        """Return a tuple of nrows, ncols."""
        return self.nrows(), self.ncols()

    def colnames(self):
        """Return a lsit of colnames."""
        return list(self.data.keys())

    def rownames(self):
        """Return a list of rownames."""
        if not self.ncols():
            return []
        val = next(iter(self.data.values()))
        if val:
            return [key for key, _ in val.iter()]
        return []

    def as_dict(self):
        """Return this matrix as a dict."""
        return {key: val.as_dict() for key, val in self.data.items()}

    def as_pandas(self):
        """Return this matrix as a pandas dataframe."""
        return pd.DataFrame.from_dict({str(key): val for key, val in self.as_dict().items()})

    def as_numpy(self):
        """Return this matrix as a numpy matrix."""
        return self.as_pandas().as_matrix()

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
        return type(self)(self.operate_cols(operator))

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
        return type(self)(outer)

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
        return type(self)(self.operate_rows(operator)).transposed()

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
