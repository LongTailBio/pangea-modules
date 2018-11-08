# pylint: disable=missing-docstring,too-few-public-methods

"""Factory for generating Ancestry models for testing."""

import factory
from pandas import DataFrame

from pangea_modules.ancestry.models import AncestryResult
from pangea_modules.ancestry_data.factory import create_values


def create_result():
    """Spoof ancestry result."""
    samples = {}
    for i in range(10):
        samples[f'Sample{i}'] = {'populations': create_values()}

    samples = DataFrame(samples).fillna(0).to_dict()
    return samples


class AncestryFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for generating Ancestry models for testing."""

    class Meta:
        """Factory metadata."""

        model = AncestryResult

    @factory.lazy_attribute
    def samples(self):  # pylint: disable=no-self-use
        """Generate random Samples."""
        return create_result()
