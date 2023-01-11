from pydantic import BaseModel, Extra
from typing import Optional, Mapping, Literal, Any


class Metadata(BaseModel, extra=Extra.forbid):
    """
    The :class:`Metadata` is a container for any metadata of the :class:`DataSchema`.

    """

    class Provenance(BaseModel, extra=Extra.forbid):
        type: str
        """Provenance type. Common values include ``'manual'`` etc."""

        metadata: Optional[Mapping[str, Any]]
        """Detailed provenance metadata in a free-form :class:`dict`."""

    version: Literal["5.0"]

    provenance: Provenance
    """Provenance of the :class:`DataSchema`."""

    timezone: str = "localtime"
    """Timezone specification.

    .. note::

        This should be set to the timezone where the measurements have been
        performed, as opposed to the timezone where ``yadg`` is being executed.
        Otherwise timezone offsets may not be accounted for correctly.

    """
