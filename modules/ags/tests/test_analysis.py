"""Test suite for Average Genome Size analysis."""

from unittest import TestCase

from pangea_modules.ags.modules import analysis_processor
from pangea_modules.microbe_census_data.factory import create_values


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
                'microbe_census': create_values(),
            }
            return sample

        samples = [create_sample(i) for i in range(15)]
        result = analysis_processor(samples)['distributions']
        self.assertIn('foo', result)
        self.assertIn('bar0', result['foo'])
        self.assertIn('bar1', result['foo'])
        self.assertEqual(5, len(result['foo']['bar0']))
