# pylint: disable=too-few-public-methods,no-self-use

"""Factory for generating KrakenHLL result models for testing."""

import os

import factory

from pangea_modules.krakenhll_data.models import KrakenHLLResult
from pangea_modules.base.utils import relative_import


model_factory = relative_import(  # pylint: disable=invalid-name
    'metaphlan2_data.factory',
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '../../metaphlan2_data/tests/factory.py')
)


def create_result(taxa_count=10, save=False):
    """Create KrakenHLL Result with specified number of taxa."""
    taxa = model_factory.create_values(taxa_count=taxa_count)
    result = KrakenHLLResult(taxa=taxa)
    if save:
        result.save()
    return result


class KrakenHLLResultFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for base ancestry data."""

    class Meta:
        """Factory metadata."""

        model = KrakenHLLResult

    @factory.lazy_attribute
    def taxa(self):
        """Return taxa."""
        return model_factory.create_values()
