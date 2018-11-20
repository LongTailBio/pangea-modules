"""Models that provide common functionality."""

from .models import (
    DataModel,
    UnlimitedGroupModel,
)


class ListModel(UnlimitedGroupModel):  # pylint: disable=too-few-public-methods
    """Represent a list with numerical indices.

    Element type may be specified but will be generic by default.
    """

    def __init__(self, dtype=DataModel):
        super().__init__(
            dtype,
            named_indices=False,
        )


class MapModel(UnlimitedGroupModel):  # pylint: disable=too-few-public-methods
    """Represent a map with numerical indices.

    Element type may be specified but will be generic by default.
    """

    def __init__(self, dtype=DataModel):
        super().__init__(
            dtype,
            named_indices=True,
        )
