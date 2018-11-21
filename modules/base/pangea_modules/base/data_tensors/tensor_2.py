"""Represent level 2 tensors."""
import pandas as pd
import numpy as np
from sklearn.manifold import TSNE

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

    def as_pandas(self):
        """Return this matrix as a pandas dataframe."""
        return pd.DataFrame.from_dict(self.data)

    def as_numpy(self):
        """Return this matrix as a numpy matrix."""
        return self.as_pandas().as_matrix()

    def as_dict(self):
        """Return this matrix as a dict."""
        return self.data

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

    def tsne(self,
             n_components=2, perplexity=30, early_exaggeration=2, learning_rate=120,
             n_iter=1000, min_grad_norm=1e-05, metric='euclidean', **kwargs):
        """Run tSNE algorithm on array of features and return labeled results."""
        params = {
            'n_components': n_components,
            'perplexity': perplexity,
            'early_exaggeration': early_exaggeration,
            'learning_rate': learning_rate,
            'n_iter': n_iter,
            'min_grad_norm': min_grad_norm,
            'metric': metric,
        }.update(kwargs)
        tsne_result = TSNE(**params).fit_transform(self.as_numpy())
        rownames, colnames = self.rownames(), self.colnames()
        new_data = {}
        for col_ind in range(n_components):
            new_data[colnames[col_ind]] = {
                rownames[row_ind]: tsne_result[row_ind][col_ind]
                for row_ind in range(self.nrows())
            }
        return Matrix(new_data)
