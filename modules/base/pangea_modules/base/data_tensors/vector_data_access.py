"""Access functionality for a vector."""

import pandas as pd

from .proxy import Proxy


class VectorAccess(Proxy):
    """Represent a sequence of numerical scalars."""

    data = pd.Series()

    def __getattr__(self, key):
        pd_attr = getattr(self.data, key)

        def wrapit(*args, **kwargs):
            """Intercept calls to pandas functions and conver to vectors."""
            pd_val = pd_attr(*args, **kwargs)
            if isinstance(pd_val, pd.Series):
                return type(self)(pd_val)
            return pd_val

        return wrapit

    def __getitem__(self, key):
        return self.data[key]

    def to_pandas(self):
        """Return a pandas series based on this vector."""
        return self.data

    def operate(self, operator):
        """Return a vector with <operator> applied to each element."""
        return type(self)({key: operator(val) for key, val in self.items()})

    def reduce(self, operator):
        """Return the function applied to the values in the vector.

        Order of values is not guaranteed.
        """
        return operator(self.get_values())
