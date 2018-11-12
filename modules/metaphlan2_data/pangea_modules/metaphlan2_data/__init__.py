"""Metaphlan 2 tool module."""

from pangea_modules.base import AnalysisModule
from pangea_modules.base.data_tensor_models import ScalarModel, VectorModel

from .constants import MODULE_NAME


class Metaphlan2ResultModule(AnalysisModule):
    """Metaphlan 2 tool module."""

    @classmethod
    def name(cls):
        """Return Metaphlan 2 module's unique identifier string."""
        return MODULE_NAME

    @classmethod
    def data_model(cls):
        """Return Metaphlan2 module's model class."""
        return VectorModel(ScalarModel(float, domain=(0, 100)))

    @classmethod
    def upload_hooks(cls):
        """Return hook for top level key, genes."""
        return [lambda payload: {'taxa': payload}]
