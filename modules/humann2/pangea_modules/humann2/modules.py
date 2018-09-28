"""HUMAnN2 tool module."""

from pangea_modules.base import SampleToolResultModule

from .constants import MODULE_NAME
from .models import Humann2Result


class Humann2ResultModule(SampleToolResultModule):
    """HUMAnN2 tool module."""

    @classmethod
    def name(cls):
        """Return HUMAnN2 module's unique identifier string."""
        return MODULE_NAME

    @classmethod
    def result_model(cls):
        """Return HUMAnN2 module's model class."""
        return Humann2Result

    @classmethod
    def upload_hooks(cls):
        """Return hook for top level key, pathways."""
        return [lambda payload: {'pathways': payload}]
