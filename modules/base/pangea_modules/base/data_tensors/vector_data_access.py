"""Access functionality for a vector."""

import pandas as pd


class VectorAccess:
    """Represent a sequence of numerical scalars."""

    data = {}

    def __getitem__(self, key):
        return self.data[key]

    def __len__(self):
        """Return the length of this vector."""
        return len(self.data)

    def as_pandas(self):
        """Return a pandas series based on this vector."""
        return pd.Series.from_dict({str(key): val for key, val in self.data.items()})

    def as_dict(self):
        """Return this vector as a dict."""
        return self.data

    def iter(self):
        """Return a generator that yields tuples of key, value."""
        for key, val in self.data.items():
            yield key, val

    def operate(self, operator):
        """Return a vector with <operator> applied to each element."""
        return type(self)({key: operator(val) for key, val in self.iter()})

    def reduce(self, operator):
        """Return the function applied to the values in the vector.

        Order of values is not guaranteed.
        """
        return operator(list(self.data.values()))
