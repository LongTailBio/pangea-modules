"""Handle data access fucntionality for matrix class."""

from .tensor_1 import Vector
from .proxy import Proxy


class MatrixAccess(Proxy):
    """Handle all data access fucntions for Matrix class."""

    def __init__(self, data, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
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

    def iterated_cols(self, operator=lambda x: x):
        """Yield tuples of key, vectors one for each col."""
        for key, col in self.iteritems():
            yield key, operator(col)

    def iterated_rows(self, operator=lambda x: x):
        """Yield key, vector pairs for each row. Ineffecient."""
        for key, row in self.iterrows():
            yield key, operator(row)

    def operated_cols(self, operator):
        """Return a dict with operator applied to each column."""
        return dict(self.iterated_cols(operator=operator))

    def operated_rows(self, operator):
        """Return a dict with operator applied to each row."""
        return dict(self.iterated_rows(operator=operator))

    def reduced_cols(self, operator):
        """Return a Vector with operator applied to each column."""
        return Vector(self.operated_cols(operator))

    def reduced_rows(self, operator):
        """Return a Vector with operator applied to each row."""
        return Vector(self.operated_rows(operator))

    def applied_cols(self, operator):
        """Return a Matrix with operator applied to each column."""
        return self.apply(operator, axis=1)

    def applied_rows(self, operator):
        """Return a Matrix with operator applied to each row."""
        return self.apply(operator, axis=0)

    def filtered_cols(self, test):
        """Return a matrix with only columns where `test` returns True.

        As input `test` is given a tuple of <column_name>, <vector>.
        """
        kept = {
            col_name: col_vals
            for col_name, col_vals in self.iterated_cols()
            if test(col_name, col_vals)
        }
        return type(self)(kept)

    def filtered_rows(self, test):
        """Return a matrix with only columns where `test` returns True.

        As input `test` is given a tuple of <column_name>, <vector>.
        """
        kept = {
            col_name: col_vals
            for col_name, col_vals in self.iterated_rows()
            if test(col_name, col_vals)
        }
        return type(self)(kept).transposed()

    def transposed(self):
        """Flip rows and columns of this matrix."""
        return self.T
