
import luigi

from shutil import rmtree
from os.path import join, dirname, isfile, isdir
from unittest import TestCase

from sample_pipeline import CountRawReads

RAW_READS_1 = join(dirname(__file__), 'data/zymo_pos_cntrl.r1.fq.gz')
RAW_READS_2 = join(dirname(__file__), 'data/zymo_pos_cntrl.r2.fq.gz')
TEST_CONFIG = join(dirname(__file__), 'data/test_config.yaml')


class TestPipelinePreprocessing(TestCase):

    def test_invoke_count_raw_reads(self):
        server_address = None  # TODO: set up local server interface
        instance = CountRawReads(
            group_name='test_group',
            sample_name='test_sample',
            server_address=server_address,
        )
        luigi.build([instance], local_scheduler=True)
