"""Handle data processing fucntionality for matrix class."""

from sklearn.manifold import TSNE

from .matrix_data_access import MatrixAccess


class MatrixProcessing(MatrixAccess):  # pylint: disable=no-member
    """Represent an unlimited group of vectors."""

    def col_means(self):
        """Return a vector with the means of each column."""
        return self.reduce_cols(lambda col: col.mean())

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
        return type(self)(new_data)
