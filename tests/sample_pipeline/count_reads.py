
from pangea_modules import PangeaSampleTarget, PangeaSampleTask
from gzip import open as gopen

from .raw_reads import RawReads


class CountRawReads(PangeaSampleTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reads = RawReads(
            group_name=self.group_name,
            sample_name=self.sample_name,
        )

    def name(self):
        return 'count_raw_reads'

    def output(self):
        target = PangeaSampleTarget(
            self.server_address,
            self.group_name,
            self.sample_name,
            self.name(),
            'read_count',
            local=self.local
        )
        return {'read_count': target}

    def requires(self):
        return self.reads

    def run(self):
        count = 0
        with gopen(self.reads.output()['reads_1'].local_path()) as i:
            for line in i:
                count += 1
        count /= 4
        target = self.output()['read_count']
        target.set_payload(count)
        target.upload()
