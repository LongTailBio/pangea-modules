"""Models for Kraken tool module."""

from mongoengine import MapField, IntField

from pangea_modules.base import ToolResult


class KrakenResult(ToolResult):     # pylint: disable=too-few-public-methods
    """Kraken tool's result type."""

    # Taxa is of the form: {<taxon_name>: <abundance_value>}
    taxa = MapField(IntField(), required=True)
