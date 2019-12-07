
from shutil import rmtree
from os import remove
from os.path import join, dirname, isfile, isdir
from unittest import TestCase
from pangea_modules import pangea_build

from .sample_pipeline import CountRawReads, ClipRawReads

from .constants import (
    SERVER_ADDRESS,
)


class TestSamplePipeline(TestCase):

    def test_invoke_count_raw_reads(self):
        instance = CountRawReads(
            group_name='my_test_group',
            sample_name='my_test_sample',
        )
        pangea_build(
            [instance],
            local_scheduler=True,
            build_local=True,
            server_address=SERVER_ADDRESS
        )
        self.assertEqual(instance.server_address, SERVER_ADDRESS)
        self.assertTrue(instance.local)
        n_reads = instance.output()['read_count'].payload
        self.assertEqual(n_reads, 1000)
        remove(join(
            dirname(__file__),
            'pangea_test/my_test_group/my_test_sample/count_raw_reads',
            'my_test_group.my_test_sample.count_raw_reads.read_count.pangea.json'
        ))

    def test_invoke_clip_raw_reads(self):
        instance = ClipRawReads(
            group_name='my_test_group',
            sample_name='my_test_sample',
        )
        pangea_build(
            [instance],
            local_scheduler=True,
            build_local=True,
            server_address=SERVER_ADDRESS
        )
        self.assertEqual(instance.server_address, SERVER_ADDRESS)
        self.assertTrue(instance.local)
        pref = join(
            dirname(__file__),
            'pangea_test/my_test_group/my_test_sample/clip_raw_reads',
            'my_test_group.my_test_sample.clip_raw_reads'
        )
        for field in ['clipped_reads_1', 'clipped_reads_2']:
            for ext in ['fastq.gz', 'pangea.json']:
                fpath = f'{pref}.{field}.{ext}'
                self.assertTrue(isfile(fpath))
                remove(fpath)
