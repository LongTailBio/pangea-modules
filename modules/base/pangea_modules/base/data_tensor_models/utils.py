"""Utilities for tensor data mdoels."""


class DictIsh:
    """Provide some dict like fucntions regardless of backer is dict or list."""

    def __init__(self, data):
        self.data = data

    def __len__(self):
        """Return the length."""
        return len(self.data)

    def __getitem__(self, key):
        """Return value from a key."""
        try:
            return self.data[key]
        except IndexError:
            raise KeyError

    def __setitem__(self, key, val):
        """Set a key value."""
        try:
            self.data[key] = val
        except IndexError:
            assert type(key) is int
            while len(self.data) < (key + 1):
                self.data.append(None)
            self[key] = val

    def items(self):
        """Return an iterator for key, value pairs."""
        try:
            return self.data.items()
        except AttributeError:
            return enumerate(self.data)

    def values(self):
        """Return an iterator for values."""
        try:
            return self.data.values()
        except AttributeError:
            return iter(self.data)

    def one_el(self):
        """Return any one element stored or None if nothing stored."""
        return next(self.values())


def flip_nested_dict(nested_dict, recurse=False):
    """Return a dict with the first two layers of keys flipped.inner_nested_dict

    If recurse is true move the outer keys as deep as possible."""
    new_outer, val = {}, None
    nested_dict = DictIsh(nested_dict)
    for key, inner_nested_dict in nested_dict.items():
        for inner_key, val in inner_nested_dict.items():
            try:
                new_outer[inner_key][key] = val
            except KeyError:
                new_outer[inner_key] = {key: val}
    if recurse and type(val) in [dict, list]:
        new_outer = {key: flip_nested_dict(val) for key, val in new_outer.items()}
    return new_outer
