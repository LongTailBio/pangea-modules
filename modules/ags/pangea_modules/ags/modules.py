"""Average Genome Size Module."""

from pangea_modules.base import AnalysisModule
from pangea_modules.base.data_tensor_models import (
    MapModel,
    ListModel,
    CategoricalModel,
    FixedGroupModel,
    VectorModel,
)
from pangea_modules.base.utils import group_samples_by_metadata
from pangea_modules.microbe_census_data import MicrobeCensusResultModule

from .constants import MODULE_NAME


def analysis_processor(*samples):
    """Handle AGS component calculations."""

    def get_ags_dist(my_samples):
        """Return vector of quartiles of ave genome size."""
        promoted = MicrobeCensusResultModule.promote_data(my_samples)
        print(promoted)
        ave_genome_size = promoted['average_genome_size']  # Vector of average genome sizes
        return ave_genome_size.quartiles()

    categories, ags_dists = group_samples_by_metadata(samples, group_apply=get_ags_dist)
    return {
        'categories': categories,
        'distributions': ags_dists,
    }


class AGSAnalysisModule(AnalysisModule):
    """AGS display module."""

    @staticmethod
    def name():
        """Return unique id string."""
        return MODULE_NAME

    @staticmethod
    def data_model():
        """Return data model class for Average Genome Size type."""
        return FixedGroupModel(
            categories=MapModel(ListModel(CategoricalModel)),
            distributions=MapModel(MapModel(VectorModel)),
        )

    @staticmethod
    def required_modules():
        """List requires ToolResult modules."""
        return [MicrobeCensusResultModule]

    @staticmethod
    def samples_processor():
        """Return function(sample_data) for proccessing AGS sample data."""
        return analysis_processor
