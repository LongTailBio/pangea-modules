"""Test suite for AnalysisModule utility tasks."""

import os
from unittest import TestCase

from pangea_modules.base.utils import (
    categories_from_metadata,
    relative_import,
)


# Base should not depend on anything; import via file as a workaround
krakenhll_data = relative_import(  # pylint: disable=invalid-name
    'pangea_modules.krakenhll_data',
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '../../krakenhll_data/pangea_modules/krakenhll_data/__init__.py'
    )
)


krakenhll_factory = relative_import(  # pylint: disable=invalid-name
    'pangea_modules.krakenhll_data.factory',
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '../../krakenhll_data/pangea_modules/krakenhll_data/factory.py'
    )
)


KRAKEN_NAME = krakenhll_data.KrakenHLLResultModule.name()


class TestDisplayModuleUtilityTasks(TestCase):
    """Test suite for Display Module utility tasks."""

    def test_categories_from_metadata(self):
        """Ensure categories_from_metadata task works."""
        metadata1 = {
            'valid_category': 'foo',
            'invalid_category': 'bar',
        }
        metadata2 = {
            'valid_category': 'baz',
        }
        sample1 = {'name': 'Sample01', 'metadata': metadata1}
        sample2 = {'name': 'Sample02', 'metadata': metadata2}
        result = categories_from_metadata([sample1, sample2])
        self.assertEqual(1, len(result.keys()))
        self.assertNotIn('invalid_category', result)
        self.assertIn('valid_category', result)
        self.assertIn('foo', result['valid_category'])
        self.assertIn('baz', result['valid_category'])
