
import luigi


class PangeaTask(luigi.Task):

    def name(self):
        raise NotImplementedError('No Module Name.')

    def ram_used(self):
        """Return an estimate of the max RAM (in GB) this task will use.

        Only needs to be set if the task uses a lot of RAM.
        """
        return 5

    def time_used(self, cores=1):
        """Return an estimate of the time the task will take in hours

        Only needs to be set if the task is slow.
        """
        return 1
