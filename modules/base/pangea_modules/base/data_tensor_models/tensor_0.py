"""Represent atomic variables."""
import mongoengine as mdb

from pangea_modules.base.data_tensors import Vector

from .models import DataModel, ModelError


class Tensor0Model:  # pylint: disable=too-few-public-methods
    """Represent a data model that defines atomic data."""
    pass


class ScalarModel(DataModel, Tensor0Model):
    """Represent a number."""

    def __init__(self, dtype=float, domain=None):
        super(ScalarModel).__init__()
        self.dtype = dtype
        self.min_val, self.max_val = None, None
        if domain:
            self.min_val, self.max_val = domain

    def get_document_class(self):  # pylint: disable=no-self-use
        """Return IntField or FloatField as appropriate."""
        if self.dtype is float:
            return mdb.FloatField(min_val=self.min_val, max_val=self.max_val)
        if self.dtype is int:
            return mdb.IntField(min_val=self.min_val, max_val=self.max_val)
        raise ModelError(f'data type {self.dtype} not available.')

    def from_son(self, son):
        """Return int or float as appropriate."""
        return self.dtype(son)

    def promote(self, observations):  # pylint: disable=no-self-use
        """Return a Vector."""
        return Vector(observations)


class CategoricalModel(DataModel, Tensor0Model):
    """Represent a string."""

    def __init__(self, options=None):
        super(CategoricalModel).__init__()
        self.options = options

    def get_document_class(self):
        """Return StringField."""
        return mdb.StringField(choices=self.options)

    def from_son(self, son):  # pylint: disable=no-self-use
        """Return the string."""
        return son
