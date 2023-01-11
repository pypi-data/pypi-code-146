from typing import Optional, Union

from pydantic import Field

from bodosdk.models.base import CamelCaseBase


class SnowflakeConnectionDefinition(CamelCaseBase):
    host: str
    port: int
    username: str
    password: str
    database: str
    warehouse: str
    role: Optional[str]


class CatalogDefinition(CamelCaseBase):
    name: str
    description: Optional[str]
    data: Union[(SnowflakeConnectionDefinition, object)]
    catalog_type: str = Field(..., alias="catalogType")


class CatalogInfo(CamelCaseBase):
    uuid: str
    name: str
    description: str
    catalog_type: str = Field(..., alias="catalogType")
    key_id: Optional[str] = Field(None, alias="keyId", hidden=True)


class CatalogUpdateDefinition(CamelCaseBase):
    description: Optional[str]
    data: Optional[object]
