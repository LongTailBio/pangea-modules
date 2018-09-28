"""Kraken tool module."""

from pangea_modules.base import SampleToolResultModule

from .constants import MODULE_NAME
from .models import KrakenHLLResult


class KrakenHLLResultModule(SampleToolResultModule):
    """Kraken tool module."""

    @classmethod
    def name(cls):
        """Return KrakenHLL module's unique identifier string."""
        return MODULE_NAME

    @classmethod
    def result_model(cls):
        """Return KrakenHLL module's model class."""
        return KrakenHLLResult

    @classmethod
    def upload_hooks(cls):
        """Return hook for top level key, taxa."""
        return [lambda payload: {'taxa': payload}]
