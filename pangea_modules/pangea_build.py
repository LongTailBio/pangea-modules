
import luigi


def pangea_build(modules, build_local=False, *args, **kwargs):
    return luigi.build(modules, *args, **kwargs)
