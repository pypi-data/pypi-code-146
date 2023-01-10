from typing import Optional

from pydantic import BaseModel, Extra


class ApiTag(BaseModel):
    """Allows adding meta data to a single tag."""

    name: str 
    """
    **REQUIRED**. The name of the tag.
    """

    description: Optional[str] = None
    """
    A short description for the tag. CommonMark syntax can be used for
    rich text representation.
    """

    class Config:
        extra = Extra.forbid
