"""Test suite for AnalysisModule utility tasks."""

from unittest import TestCase

from pangea_modules.krakenhll_data import KrakenHLLResultModule
from pangea_modules.krakenhll_data.factory import create_result

from pangea_modules.base.utils import (
    categories_from_metadata,
    collate_samples,
)


KRAKEN_NAME = KrakenHLLResultModule.name()


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

    def test_collate_samples(self):
        """Ensure collate_samples task works."""
        sample1 = {
            'name': 'Sample01',
            KRAKEN_NAME: create_result(save=False),
        }
        sample2 = {
            'name': 'Sample02',
            KRAKEN_NAME: create_result(save=False),
        }
        samples = [sample1, sample2]
        result = collate_samples(KRAKEN_NAME, ['taxa'], samples)
        self.assertIn('Sample01', result)
        self.assertIn('Sample02', result)
        self.assertIn('taxa', result['Sample01'])
        self.assertIn('taxa', result['Sample02'])
