# pylint disable=too-many-ancestors

"""Access functionality for a vector."""

import pandas as pd


class VectorAccess(pd.Series):  # pylint disable=too-many-ancestors
    """Represent a sequence of numerical scalars."""

    def __getattribute__(self, key):
        my_attr = getattr(self, key)

        def wrapit(*args, **kwargs):
            """Intercept calls to pandas functions and conver to vectors."""
            pd_val = my_attr(*args, **kwargs)
            if isinstance(pd_val, type(self)):
                return pd_val
            if isinstance(pd_val, pd.Series):
                return type(self)(pd_val)
            return pd_val

        return wrapit

    def operate(self, operator):
        """Return a vector with <operator> applied to each element."""
        return type(self)({key: operator(val) for key, val in self.items()})

    def reduce(self, operator):
        """Return the function applied to the values in the vector.

        Order of values is not guaranteed.
        """
        return operator(self.get_values())
