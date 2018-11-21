# pylint: disable=too-few-public-methods,no-self-use

"""Factory for generating KrakenHLL result models for testing."""

import factory

from pangea_modules.base.utils.factory import create_taxa_values
from pangea_modules.krakenhll_data import KrakenHLLResultModule


def create_result(taxa_count=10):
    """Create KrakenHLL Result with specified number of taxa."""
    taxa = create_taxa_values(taxa_count=taxa_count)
    result = KrakenHLLResultModule.data_model().from_son({'taxa': taxa})
    return result


class KrakenHLLResultFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for base ancestry data."""

    class Meta:
        """Factory metadata."""

        model = KrakenHLLResultModule.result_model()

    @factory.lazy_attribute
    def taxa(self):
        """Return taxa."""
        return create_taxa_values()
