from pydantic import BaseModel, Extra
from typing import Literal, Optional, Union


class ExternalDateFile(BaseModel, extra=Extra.forbid):
    """Read external date information from file."""

    class Content(BaseModel, extra=Extra.forbid):
        path: str
        """Path to the external date information file."""

        type: str
        """Type of the external date information file."""

        match: Optional[str]
        """String to be matched within the file."""

    file: Content


class ExternalDateFilename(BaseModel, extra=Extra.forbid):
    """Read external date information from the file name."""

    class Content(BaseModel, extra=Extra.forbid):
        format: str
        """``strptime``-like format string for processing the date."""

        len: int
        """Number of characters from the start of the filename to parse."""

    filename: Content


class ExternalDateISOString(BaseModel, extra=Extra.forbid):
    """Read a constant external date using an ISO-formatted string."""

    isostring: str


class ExternalDateUTSOffset(BaseModel, extra=Extra.forbid):
    """Read a constant external date using a Unix timestamp offset."""

    utsoffset: float


class ExternalDate(BaseModel, extra=Extra.forbid):
    """Supply timestamping information that are external to the processed file."""

    using: Union[
        ExternalDateFile,
        ExternalDateFilename,
        ExternalDateISOString,
        ExternalDateUTSOffset,
    ]
    """Specification of the external date format."""

    mode: Literal["add", "replace"] = "add"
    """Whether the external timestamps should be added to or should replace the 
    parsed data."""
