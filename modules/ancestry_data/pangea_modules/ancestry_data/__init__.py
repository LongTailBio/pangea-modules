"""Ancestry tool module."""

from pangea_modules.base import AnalysisModule
from pangea_modules.base.data_tensor_models import ScalarModel, VectorModel

from .constants import MODULE_NAME, KNOWN_LOCATIONS


class AncestryResultModule(AnalysisModule):
    """Ancestry tool module."""

    @classmethod
    def name(cls):
        """Return Ancestry module's unique identifier string."""
        return MODULE_NAME

    @classmethod
    def data_model(cls):
        """Return Ancestry module's model class."""
        return VectorModel(ScalarModel(domain=(0, 1)), allowed_keys=KNOWN_LOCATIONS)

    @classmethod
    def upload_hooks(cls):
        """Return hook for top level key."""
        return [lambda payload: {'populations': payload}]
