"""Tasks for generating Sample Similarity results."""

from pangea_modules.base.utils import scrub_category_val, categories_from_metadata
from pangea_modules.krakenhll_data import KrakenHLLResultModule
from pangea_modules.metaphlan2_data import Metaphlan2ResultModule


def taxa_tool_tsne(samples, tool):
    """Run tSNE for tool results stored as 'taxa' property."""
    axis_labels = [f'{tool.name()} tsne x', f'{tool.name()} tsne y']
    print(tool.promote_data(samples))
    taxa_matrix = tool.promote_data(samples)['taxa']
    taxa_tsne = taxa_matrix.tsne()
    taxa_tsne = {axis_labels[i]: axis for i, axis in taxa_tsne.iter_cols()}

    return taxa_tsne


def processor(*samples):
    """Combine Sample Similarity components."""
    kraken_tsne = taxa_tool_tsne(samples, KrakenHLLResultModule)
    mphlan_tsne = taxa_tool_tsne(samples, Metaphlan2ResultModule)

    return {
        'categories': categories_from_metadata(samples),
        'tools': {
            KrakenHLLResultModule.name(): kraken_tsne,
            Metaphlan2ResultModule.name(): mphlan_tsne,
        },
        'data_records': {
            sample['name']: {
                category_name: scrub_category_val(category_value)
                for category_name, category_value in sample['metadata'].items()
            }
            for sample in samples
        },
    }
