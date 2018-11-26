"""Tasks for generating Top Taxa Size results."""

from pangea_modules.base.utils import group_samples_by_metadata
from pangea_modules.krakenhll_data import KrakenHLLResultModule
from pangea_modules.metaphlan2_data import Metaphlan2ResultModule


KRAKENHLL = KrakenHLLResultModule
METAPHLAN = Metaphlan2ResultModule


def filter_taxa_by_kingdom(taxa_matrix, kingdom):
    """Return taxa in the given kingdom."""
    if kingdom == 'all_kingdoms':
        return taxa_matrix.filter_cols(lambda taxa_name, _: 's__' in taxa_name.split('|')[-1])
    raise ValueError(f'Kingdom {kingdom} not found.')


def processor(samples):
    """Return top taxa organized by metadata and kingdoms."""

    def group_apply(my_samples):
        out = {}
        for tool in [KRAKENHLL, METAPHLAN]:
            out[tool.name()] = {}
            taxa_matrix = tool.promote_data(my_samples)['taxa'].as_compositional()
            for kingdom in ['all_kingdoms']:
                kingdom_taxa_matrix = filter_taxa_by_kingdom(taxa_matrix, kingdom)
                out[tool.name()][kingdom] = {
                    'abundance': kingdom_taxa_matrix.col_means(),
                    'prevalence': kingdom_taxa_matrix.operate_cols(lambda col: col.num_non_zero()),
                }
        return out

    _, top_taxa = group_samples_by_metadata(samples, group_apply=group_apply)
    return {'categories': top_taxa}
