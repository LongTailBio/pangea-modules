"""Kraken tool module."""

from pangea_modules.base import AnalysisModule
from pangea_modules.base.data_tensor_models import (
    ScalarModel,
    VectorModel,
    FixedGroupModel,
)
from .constants import MODULE_NAME


class KrakenHLLResultModule(AnalysisModule):
    """Kraken tool module."""

    @classmethod
    def name(cls):
        """Return Kraken module's unique identifier string."""
        return MODULE_NAME

    @classmethod
    def data_model(cls):
        """Return Kraken module's model class."""
        return FixedGroupModel(
            taxa=VectorModel(ScalarModel(float, domain=(0, 100))),
        )

    @classmethod
    def upload_hooks(cls):
        """Return hook for top level key, taxa."""
        return [lambda payload: {'taxa': payload}]
