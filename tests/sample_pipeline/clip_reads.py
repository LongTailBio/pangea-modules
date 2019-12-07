
import luigi
from pangea_modules import PangeaTarget, PangeaTask
from gzip import open as gopen

from .raw_reads import RawReads

CLIP_LEN = 31


class ClipRawReads(PangeaTask):
    group_name = luigi.Parameter()
    sample_name = luigi.Parameter()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reads = RawReads(
            group_name=self.group_name,
            sample_name=self.sample_name,
        )

    def name(self):
        return 'clip_raw_reads'

    def output(self):
        reads1 = PangeaTarget(
            self.server_address,
            self.group_name,
            self.sample_name,
            self.name(),
            'clipped_reads_1',
            local=self.local,
            is_s3=True,
            ext='fastq.gz'
        )
        reads2 = PangeaTarget(
            self.server_address,
            self.group_name,
            self.sample_name,
            self.name(),
            'clipped_reads_2',
            local=self.local,
            is_s3=True,
            ext='.fastq.gz'
        )
        reads1.makedirs()
        return {'reads_1': reads1, 'reads_2': reads2}

    def requires(self):
        return self.reads

    def run(self):
        for key in ['reads_1', 'reads_2']:
            reads_in = self.reads.output()[key].local_path()
            target = self.output()[key]
            reads_out = target.local_path()
            with gopen(reads_in) as ifile, gopen(reads_out, 'w') as ofile:
                for i, line in enumerate(ifile):
                    if (i % 4) == 1:
                        line = line[:CLIP_LEN] + b'\n'
                    ofile.write(line)
            target.set_payload(reads_out)
            target.upload()
