"""Test suite for Average Genome Size analysis."""

import os
from unittest import TestCase

from pangea_modules.ags.analysis import ags_distributions
from pangea_modules.base.utils import relative_import


factory = relative_import(  # pylint: disable=invalid-name
    'factory',
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '../../microbe_census_data/tests/factory.py')
)


class TestAverageGenomeSizeTasks(TestCase):
    """Test suite for Average Genome Size analysis."""

    def test_ags_distributions(self):
        """Ensure ags_distributions analysis works."""

        def create_sample(i):
            """Create test sample."""
            metadata = {'foo': f'bar{i}'}
            sample = {
                'name': f'SMPL_{i}',
                'metadata': metadata,
                'microbe_census': factory.create_values(),
            }
            return sample

        samples = [create_sample(i) for i in range(15)]
        result = ags_distributions(samples)
        self.assertIn('foo', result)
        self.assertIn('bar0', result['foo'])
        self.assertIn('bar1', result['foo'])
        self.assertIn('min_val', result['foo']['bar0'])
