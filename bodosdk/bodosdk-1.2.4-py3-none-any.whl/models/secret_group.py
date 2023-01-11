from typing import Optional

from bodosdk.models.base import CamelCaseBase


class SecretGroupDefinition(CamelCaseBase):
    name: str
    description: Optional[str]


class SecretGroupInfo(CamelCaseBase):
    uuid: str
    name: str
    description: str
