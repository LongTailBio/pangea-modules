
import luigi
from pangea_modules import PangeaTarget, PangeaTask


class RawReads(PangeaTask):
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
            'reads_1',
            local=self.local,
            is_s3=True,
        )
        read2 = PangeaTarget(
            self.server_address,
            self.group_name,
            self.sample_name,
            self.name(),
            'reads_2',
            local=self.local,
            is_s3=True,
        )
        read1.makedirs()
        return {
            'reads_1': read1,
            'reads_2': read2
        }

    def run(self):
        pass
