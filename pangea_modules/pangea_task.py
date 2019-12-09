
import luigi

from .network import (
    PangeaServerInterface,
    LocalPangeaServerInterface,
)


class PangeaTask(luigi.Task):

    def name(self):
        raise NotImplementedError('No Module Name.')

    def _iter_pangea_requires(self):
        try:
            for module in self.requires():
                if isinstance(module, PangeaTask):
                    yield module
        except TypeError:
            module = self.requires()
            if isinstance(module, PangeaTask):
                yield module

    def set_server_address(self, server_address, local=False):
        self.server_address = server_address
        if local:
            self.server = LocalPangeaServerInterface.from_address(server_address)
        else:
            self.server = PangeaServerInterface.from_address(server_address)
        self.set_local(local=local)
        for module in self._iter_pangea_requires():
            module.set_server_address(server_address, local=local)

    def set_local(self, local=True):
        self.local = local
        for module in self._iter_pangea_requires():
            module.set_local(local=local)

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


class PangeaGroupTask(PangeaTask):
    group_name = luigi.Parameter()

    def sample_names(self):
        """Return a list of sample names in this group."""
        return self.server.get_samples_in_group(self.group_name)


class PangeaSampleTask(PangeaTask):
    group_name = luigi.Parameter()
    sample_name = luigi.Parameter()
