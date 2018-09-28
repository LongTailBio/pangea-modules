"""Factory for generating Kraken result models for testing."""

from random import randint, random

from pangea_modules.humann2 import Humann2Result


def create_values():
    """Create a plausible humann2 values object."""
    path_names = [f'sample_pathway_{i}' for i in range(randint(3, 100))]
    result = {
        'pathway_abundances': {
            path_name: 100 * random() for path_name in path_names
        },
        'pathway_coverages': {
            path_name: random() for path_name in path_names
        },
    }
    return result


def create_result(save=True):
    """Create Humann2Result with randomized field data."""
    packed_data = create_values()
    result = Humann2Result(**packed_data)
    if save:
        result.save()
    return result
