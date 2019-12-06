
import luigi

from shutil import rmtree
from os.path import join, dirname, isfile, isdir
from unittest import TestCase

from .sample_pipeline import CountRawReads

from .constants import (
    SERVER_ADDRESS,
    RAW_READS_1,
)


class TestSamplePipeline(TestCase):

    def test_invoke_count_raw_reads(self):
        instance = CountRawReads(
            group_name='test_group',
            sample_name='test_sample',
            server_address=SERVER_ADDRESS,
        )
        instance.reads.output()['reads_1']._local_path = RAW_READS_1
        print(instance.output()['read_count'])
        luigi.build([instance], local_scheduler=True)
        print(instance.output()['read_count'])
        n_reads = instance.output()['read_count'].payload
        self.assertEqual(n_reads, 1000)
