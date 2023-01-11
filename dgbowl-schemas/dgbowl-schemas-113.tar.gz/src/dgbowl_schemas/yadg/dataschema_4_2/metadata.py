from pydantic import BaseModel, Extra
from typing import Optional, Mapping, Literal, Any


class Metadata(BaseModel, extra=Extra.forbid):
    """Metadata, including version and provenance of the :class:`DataSchema`."""

    class Provenance(BaseModel, extra=Extra.forbid):
        type: str
        metadata: Optional[Mapping[str, Any]]

    version: Literal["4.2"]

    provenance: Provenance
    """Provenance information."""

    timezone: str = "localtime"
    """Timezone specification.

    .. note::

        This should be set to the timezone where the measurements have been
        performed, as opposed to the timezone where yadg is being executed,
        otherwise timezone offsets may not be accounted for correctly.

    """
