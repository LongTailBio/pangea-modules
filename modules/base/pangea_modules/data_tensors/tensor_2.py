
import pandas as pd

from .tensor_1 import Vector


class Tensor2:
    """Represent a group of groups of atomic data."""
    pass


class VectorGroup(Tensor2):

    def __init__(self, **vectors):
        self.vectors = vectors

    def __get__(self, key):
        return self.vectors[key]


class Matrix(Tensor2):

    def __init__(self, data):
        self.data = data
        if type(data) is list:
            self.data = {ind: val for ind, val in enumerate(data)}

    def __get__(self, key):
        return self.data[key]

    def ncols(self):
        """Return the number of columns in this matrix."""
        return len(self.data)

    def nrows(self):
        """Return the number of rows in this matrix."""
        val = len(next(self.data.values()))
        if val is None:
            return 0
        return val

    def as_pandas(self):
        """Return this matrix as a pandas dataframe."""
        return pd.DataFrame.from_dict(self.data)

    def iter_cols(self, operator=lambda x: x):
        """Yield tuples of key, vectors one for each col."""
        for key, col in self.data.items():
            yield key, operator(col)

    def transpose(self):
        """Flip rows and columns of this matrix."""
        outer = {}
        for col_name, row in self.data.items():
            for row_name, val in row.items():
                try:
                    outer[row_name][col_name] = val
                except KeyError:
                    outer[row_name] = {col_name: val}
        outer = {row_name: Vector(row) for row_name, row in outer.items()}
        return Matrix(outer)

    def iter_rows(self, operator=lambda x: x):
        """Yield key, vector pairs for each row. Ineffecient."""
        return self.transpose().iter_cols(operator=operator)

    def col_means(self):
        """Return a vector with the means of each column."""
        data = self.iter_cols(operator=lambda col: col.mean())
        return Vector(data, indexed=self.col_indexed)

    def row_means(self):
        """Return a vector with means for each row."""
        return self.transpose().col_means()
