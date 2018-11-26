"""Test suite for Sample Similarity tasks."""

from uuid import uuid4
from unittest import TestCase

from pangea_modules.krakenhll_data import KrakenHLLResultModule
from pangea_modules.krakenhll_data.factory import create_result
from pangea_modules.sample_similarity.analysis import taxa_tool_tsne


KRAKEN_NAME = KrakenHLLResultModule.name()


class TestSampleSimilarityTasks(TestCase):
    """Test suite for Sample Similarity tasks."""

    def test_taxa_tool_tsne(self):
        """Ensure taxa_tool_tsne task returns correct results."""

        def create_sample(i):
            """Create unique sample for index."""
            sample_data = {
                'name': f'SMPL_{i}',
                'library_uuid': uuid4(),
                KRAKEN_NAME: create_result(),
            }
            return sample_data

        samples = [create_sample(i) for i in range(3)]
        taxa_tsne = taxa_tool_tsne(samples, KrakenHLLResultModule)
        self.assertIn(f'{KRAKEN_NAME} tsne x', taxa_tsne)
        self.assertIn(f'{KRAKEN_NAME} tsne y', taxa_tsne)
