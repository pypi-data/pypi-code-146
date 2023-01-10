from pydantic import Extra, Field

from aiosox.utils import BaseModel


class Reference(BaseModel):

    ref: str = Field(alias="$ref")

    class Config:
        extra = Extra.forbid
