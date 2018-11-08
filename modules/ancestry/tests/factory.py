# pylint: disable=missing-docstring,too-few-public-methods

"""Factory for generating Ancestry models for testing."""

import os

import factory
from pandas import DataFrame

from pangea_modules.ancestry.models import AncestryResult
from pangea_modules.base.utils import relative_import


factory = relative_import(  # pylint: disable=invalid-name
    'factory',
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '../../ancestry_data/tests/factory.py')
)


def create_result():
    """Spoof ancestry result."""
    samples = {}
    for i in range(10):
        samples[f'Sample{i}'] = {'populations': factory.create_values()}

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
