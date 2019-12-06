
import luigi
from pangea_modules import PangeaTarget, PangeaTask

from ..constants import RAW_READS_1, RAW_READS_2


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
            'reads_1',
            local_path=RAW_READS_1
        )
        read1._local_path = RAW_READS_1
        read2 = PangeaTarget(
            self.server_address,
            self.group_name,
            self.sample_name,
            self.name(),
            'reads_2',
            local_path=RAW_READS_2
        )
        read1._local_path = RAW_READS_2
        read1.makedirs()
        return {
            'reads_1': read1,
            'reads_2': read2
        }

    def run(self):
        pass
