
import luigi
from pangea_modules import PangeaTarget, PangeaTask
from gzip import open as gopen

from .raw_reads import RawReads


class CountRawReads(PangeaTask):
    server_address = luigi.Parameter()
    group_name = luigi.Parameter()
    sample_name = luigi.Parameter()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reads = RawReads(
            server_address=self.server_address,
            group_name=self.group_name,
            sample_name=self.sample_name,
        )

    def name(self):
        return 'count_raw_reads'

    def output(self):
        target = PangeaTarget(
            self.server_address,
            self.group_name,
            self.sample_name,
            self.name(),
            'read_count',
        )
        target.makedirs()
        return {'read_count': target}

    def requires(self):
        return self.reads

    def run(self):
        count = 0
        with gopen(self.reads['reads_1'].local_path()) as i:
            for line in i:
                count += 1
        count /= 4
        target = self.output()['read_counts']
        target.set_payload(count)
        target.upload()
