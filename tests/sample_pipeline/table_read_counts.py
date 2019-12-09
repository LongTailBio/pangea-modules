
from pangea_modules import PangeaGroupTarget, PangeaGroupTask

from .count_reads import CountRawReads


class TableReadCounts(PangeaGroupTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._read_counts = None

    @property
    def read_counts(self):
        if self._read_counts:
            return self._read_counts
        self._read_counts = [
            CountRawReads(self.group_name, sample_name)
            for sample_name in self.sample_names()
        ]
        return self._read_counts

    def name(self):
        return 'table_read_counts'

    def output(self):
        target = PangeaGroupTarget(
            self.server_address,
            self.group_name,
            self.name(),
            'read_counts',
            local=self.local
        )
        return {'read_counts': target}

    def requires(self):
        return self.read_counts

    def run(self):
        counts = {}
        for read_counter in self.read_counts:
            counts[read_counter.sample_name] = read_counter.output()['read_count'].payload
        target = self.output()['read_counts']
        target.set_payload(counts)
        target.upload()
