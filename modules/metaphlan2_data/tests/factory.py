# pylint: disable=too-few-public-methods,no-self-use

"""Factory for generating Metaphlan2 result models for testing."""

import random
import factory

from pangea_modules.base.factory_utils import create_taxa_values
from pangea_modules.metaphlan2_data.models import Metaphlan2Result


def create_result(taxa_count=10, save=False):
    """Create Metaphlan2Result with specified number of taxa."""
    taxa = create_taxa_values(taxa_count=taxa_count)
    result = Metaphlan2Result(taxa=taxa)
    if save:
        result.save()
    return result


class Metaphlan2ResultFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for base ancestry data."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Factory metadata."""

        model = Metaphlan2Result

    @factory.lazy_attribute
    def taxa(self):  # pylint: disable=no-self-use
        """Return taxa."""
        return create_taxa_values()
