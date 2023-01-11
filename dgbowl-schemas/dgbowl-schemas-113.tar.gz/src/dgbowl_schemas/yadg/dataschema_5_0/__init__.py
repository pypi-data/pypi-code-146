from pydantic import BaseModel, Extra
from typing import Sequence
from .metadata import Metadata
from .step import Steps


class DataSchema(BaseModel, extra=Extra.forbid):
    """
    :class:`DataSchema` introduced in ``yadg-5.0``.
    """

    metadata: Metadata
    """Input metadata for ``yadg``."""

    steps: Sequence[Steps]
    """Input commands for ``yadg``'s parsers, organised as a sequence of steps."""
