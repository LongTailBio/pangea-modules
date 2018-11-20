"""Core models for tensor data."""

import mongoengine as mdb

from .utils import flip_nested_dict


class TensorTypeError(TypeError):
    """Represent an error with a model."""
    pass


class DataModel:
    """Base class for data models."""

    def get_document_class(self):  # pylint: disable=no-self-use
        """Return the mongodb class matching this model."""
        raise NotImplementedError()

    def validate(self):  # pylint: disable=no-self-use
        """Return a 'clean' function for the mongodb class."""
        return None

    def from_son(self, son):  # pylint: disable=no-self-use
        """Return an instantiated data type from SON input."""
        raise NotImplementedError()

    def promote(self, observations):  # pylint: disable=no-self-use
        """Return a promoted version of this model."""
        raise NotImplementedError()


class MongoWrapperModel(DataModel):
    """Wrap a mongoengine field directly."""

    def __init__(self, mdb_model):
        self.model = mdb_model

    def get_document_class(self):
        """Return the stored model."""
        return self.model

    def from_son(self, son):  # pylint: disable=no-self-use
        """Return the SON as is."""
        return son

    def promote(self, observations):  # pylint: disable=no-self-use
        """Return observations as is."""
        return observations


class FixedGroupModel(DataModel):
    """Fixed Groups have a predefined number of named parameters.

    Each parameter can be a different DataModel.
    """

    def __init__(self, model=None, return_type=None, **dtypes: {str: DataModel}):
        super()
        self.return_type = return_type
        self.dtypes = dtypes
        for val in self.dtypes.values():
            if model and not isinstance(val, model):
                raise TensorTypeError()

    def get_document_class(self):
        """Return an anonymous Field Class with subfields as specified."""
        return type(
            '',
            (mdb.EmbeddedDocumentField,),
            {key: val.get_document_class() for key, val in self.dtypes.items()}
        )

    def from_son(self, son):
        """Return a dict mapping keys to objects."""
        recursed = {
            key: self.dtypes[key].from_son(val)
            for key, val in son.items()
        }
        if self.return_type:
            return self.return_type(recursed)
        return recursed

    def promote(self, observations):
        """Return a promoted version of this group."""
        outer = {}
        if isinstance(observations, dict):
            for key, dtype in self.dtypes.items():
                inner = {sample: observation[key] for sample, observation in observations.items()}
                outer[key] = dtype.promote(inner)
        else:
            for key, dtype in self.dtypes.items():
                inner = [observation[key] for observation in observations]
                outer[key] = dtype.promote(inner)
        return outer


class UnlimitedGroupModel(DataModel):
    """Unlimited Groups may have any number of parameters.

    Parameters may be named (dict) or numbered (list).
    """

    def __init__(self, dtype, named_indices=True, return_type=None, allowed_keys=None):
        super()
        self.named_indices = named_indices
        self.return_type = return_type
        self.dtype = dtype
        self.allowed_keys = allowed_keys  # doesn't do anything yet, will limit keys

    def get_document_class(self):
        """Return a Map or List Field as appropriate."""
        sub_class = self.dtype.get_document_class()
        if self.named_indices:
            return mdb.MapField(field=sub_class)
        return mdb.ListField(field=sub_class)

    def from_son(self, son):
        """Return a dict or list with sub objects as appropriate."""
        if self.named_indices:
            recursed = {key: self.dtype.from_son(val) for key, val in son.items()}
        else:
            recursed = [self.dtype.from_son(val) for val in son]
        if self.return_type:
            recursed = self.return_type(recursed)
        return recursed

    def promote(self, observations):
        """Return a promoted version of this group."""
        flipped = flip_nested_dict(observations)
        flipped = {key: self.dtype.promote(val) for key, val in flipped.items()}
        return flipped
