from typing import Optional

from pydantic import Field

from bodosdk.models.base import CamelCaseBase


class SecretDefinition(CamelCaseBase):
    name: str
    data: object
    secret_group: Optional[str] = Field(None, alias="secretGroup")
    secret_type: Optional[str] = Field(None, alias="secretType")


class SecretInfo(CamelCaseBase):
    uuid: str
    name: str
    secret_group: str = Field(alias="secretGroup")
    secret_type: str = Field(alias="secretType")
