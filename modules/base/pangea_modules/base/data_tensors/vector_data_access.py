"""Access functionality for a vector."""

from .proxy import Proxy


class VectorAccess(Proxy):
    """Represent a sequence of numerical scalars."""

    def __init__(self, data, *args, **kwargs):
        super().__init__(data, *args, **kwargs)

    def to_pandas(self):
        """Return a pandas series based on this vector."""
        return self._obj

    def operated(self, operator):
        """Return a vector with <operator> applied to each element."""
        return type(self)({key: operator(val) for key, val in self.items()})

    def reduced(self, operator):
        """Return the function applied to the values in the vector.

        Order of values is not guaranteed.
        """
        return operator(self.get_values())
