# pylint: disable=missing-docstring,too-few-public-methods

"""Factory for generating Top Taxa models for testing."""

import os
from random import random

import factory

from pangea_modules.base.utils import relative_import
from pangea_modules.krakenhll_data import KrakenHLLResultModule
from pangea_modules.metaphlan2_data import Metaphlan2ResultModule
from pangea_modules.top_taxa.models import TopTaxaResult


krakenhll_factory = relative_import(  # pylint: disable=invalid-name
    'krakenhll_data.factory',
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '../../krakenhll_data/tests/factory.py')
)


metaphlan2_factory = relative_import(  # pylint: disable=invalid-name
    'metaphlan2_data.factory',
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '../../metaphlan2_data/tests/factory.py')
)


KRAKENHLL = KrakenHLLResultModule.name()
METAPHLAN = Metaphlan2ResultModule.name()


def create_values():
    """Return values for top taxa sample."""
    return {
        KRAKENHLL: krakenhll_factory.create_result(),
        METAPHLAN: metaphlan2_factory.create_result(),
    }


def factory_abundance():
    """Return fake abunds and prevs."""
    return {
        'abundance': {
            'taxa_1': random(),
            'taxa_2': random(),
            'taxa_3': random(),
        },
        'prevalence': {
            'taxa_1': random(),
            'taxa_2': random(),
            'taxa_3': random(),
        }

    }


def factory_tools():
    """Return fake tools."""
    return {
        KRAKENHLL: {
            'all_kingdoms': factory_abundance(),
        },
        METAPHLAN: {
            'all_kingdoms': factory_abundance(),
        },
    }


class TopTaxaFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for Analysis Result's Sample Similarity."""

    class Meta:
        """Factory metadata."""

        model = TopTaxaResult

    categories = {
        'foo': {
            'foo_1': factory_tools(),
            'foo_2': factory_tools(),
        },
        'bar': {
            'bar_1': factory_tools(),
            'bar_2': factory_tools(),
        },
    }
