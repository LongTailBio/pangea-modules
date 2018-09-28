"""HUMAnN2 tool module."""

from mongoengine import FloatField, MapField

from pangea_modules.base import ToolResult


class Humann2Result(ToolResult):  # pylint: disable=too-few-public-methods
    """HUMAnN2 result type."""

    pathway_abundances = MapField(field=FloatField(), required=True)
    pathway_coverages = MapField(field=FloatField(), required=True)

    @classmethod
    def vector_variables(cls):
        """Return names of variables that are vectors."""
        return ['pathway_abundances', 'pathway_coverages']
