"""Functions for generating Average Genome Size results."""

from pangea_modules.base.utils import boxplot, categories_from_metadata
from pangea_modules.microbe_census_data import MicrobeCensusResultModule


def ags_distributions(samples):
    """Determine Average Genome Size distributions."""
    microbe_census_key = MicrobeCensusResultModule.name()
    ags_vals = {}
    for sample in samples:
        sample_ags = sample[microbe_census_key]['average_genome_size']
        for key, value in sample['metadata'].items():
            try:
                ags_vals[key][value].append(sample_ags)
            except KeyError:
                try:
                    ags_vals[key][value] = [sample_ags]
                except KeyError:
                    ags_vals[key] = {value: [sample_ags]}

    for category, val_dict in ags_vals.items():
        for val, ags_values in val_dict.items():
            ags_vals[category][val] = boxplot(ags_values)

    return ags_vals


def processor(*samples):
    """Handle AGS component calculations."""
    categories = categories_from_metadata(samples)
    ags_dists = ags_distributions(samples)
    result = {
        'categories': categories,
        'distributions': ags_dists,
    }
    return result