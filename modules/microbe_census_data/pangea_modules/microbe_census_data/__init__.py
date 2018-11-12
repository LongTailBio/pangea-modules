"""Microbe Census tool module."""

from pangea_modules.base import AnalysisModule
from pangea_modules.base.data_tensor_models import (
    ScalarModel,
    FixedGroupModel,
)


class MicrobeCensusResultModule(AnalysisModule):
    """Microbe Census tool module."""

    @classmethod
    def name(cls):
        """Return Microbe Census module's unique identifier string."""
        return 'microbe_census'

    @classmethod
    def data_model(cls):
        """Return Microbe Census module's model class."""
        return FixedGroupModel(
            average_genome_size=ScalarModel(domain=(0, None)),
            total_bases=ScalarModel(dtype=int, domain=(0, None)),
            genome_equivalents=ScalarModel(domain=(0, None))
        )
