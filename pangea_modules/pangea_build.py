
import luigi

from .pangea_task import PangeaTask


def pangea_build(modules, server_address=None, build_local=False, *args, **kwargs):
    for module in modules:
        if isinstance(module, PangeaTask):
            module.set_server_address(server_address, local=build_local)
    return luigi.build(modules, *args, **kwargs)
