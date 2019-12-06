
import luigi
from pangea_modules import PangeaTarget, PangeaTask


class RawReads(PangeaTask):
    server_address = luigi.Parameter()
    group_name = luigi.Parameter()
    sample_name = luigi.Parameter()

    def name(self):
        return 'raw_reads'

    def output(self):
        read1 = PangeaTarget(
            self.server_address,
            self.group_name,
            self.sample_name,
            self.name(),
            'read_1',
        )
        read2 = PangeaTarget(
            self.server_address,
            self.group_name,
            self.sample_name,
            self.name(),
            'read_1',
        )
        read1.makedirs()
        return {
            'read_1': read1,
            'read_2': read2
        }

    def run(self):
        pass
