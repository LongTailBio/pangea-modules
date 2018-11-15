"""Tasks to process Ancestry results."""

from pandas import DataFrame

from pangea_modules.base.utils import collate_samples
from pangea_modules.ancestry_data import AncestryResultModule

from .constants import TOOL_MODULE_NAME


def processor(*samples):
    """Handle Ancestry component calculations."""
    fields = list(AncestryResultModule.result_model()._fields.keys())  # pylint:disable=no-member
    collate_fields = [field for field in fields if not field == 'id']
    samples = collate_samples(TOOL_MODULE_NAME, collate_fields, samples)
    framed_samples = DataFrame(samples).fillna(0).to_dict()
    result = {'samples': framed_samples}
    return result
