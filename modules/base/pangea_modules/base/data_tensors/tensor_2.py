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

    def col_means(self):
        """Return a vector with the means of each column."""
        data = dict(self.iter_cols(operator=lambda col: col.mean()))
        return Vector(data)

    def row_means(self):
        """Return a vector with means for each row."""
        return self.transposed().col_means()
