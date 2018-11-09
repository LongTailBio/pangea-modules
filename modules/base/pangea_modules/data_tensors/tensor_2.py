
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

    def __init__(self, data, row_indexed=True, col_indexed=True):
        self.data = data
        self.row_indexed, self.col_indexed = row_indexed, col_indexed

    def __get__(self, key):
        return self.data[key]

    def ncols(self):
        """Return the number of columns in this matrix."""
        return len(self.data)

    def nrows(self):
        """Return the number of rows in this matrix."""
        if self.ncols() == 0:
            return 0
        if not self.col_indexed:
            return len(self.data[0])
        for val in self.data.values():
            return len(val)

    def as_pandas(self):
        """Return this matrix as a pandas dataframe."""
        return pd.DataFrame.from_dict(self.data)

    def iter_cols(self, operator=lambda x: x):
        """Yield tuples of key, vectors one for each col."""
        if self.col_indexed:
            for key, col in self.data.items():
                yield key, operator(col)
        else:
            for ind, col in enumerate(self.data):
                yield ind, operator(col)

    def transpose(self):
        """Flip rows and columns of this matrix."""
        outer = []
        if self.row_indexed:
            outer = {}
        if self.col_indexed:
            for col_name, row in self.data:
                if self.row_indexed:
                    for row_name, val in row.iter():
                        try:
                            outer[row_name][col_name] = val
                        except KeyError:
                            outer[row_name] = {col_name: val}
                else:
                    for _, val in row.iter():
                        try:
                            outer[row_name].append(val)
                        except KeyError:
                            outer[row_name] = [val]
        else:
            for ind, row in enumerate(self.data):
                if self.row_indexed:
                    for row_name, val in row.iter():
                        try:
                            outer[ind][col_name] = val
                        except IndexError:
                            outer.append({col_name: val})
                else:
                    for _, val in row.iter():
                        try:
                            outer[ind].append(val)
                        except IndexError:
                            outer.append([val])
        return Matrix(outer, row_indexed=self.col_indexed, col_indexed=self.row_indexed)

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
