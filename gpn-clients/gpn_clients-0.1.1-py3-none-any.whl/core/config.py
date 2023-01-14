from typing import Optional, Union

from pydantic import (
    BaseModel,
    Field,
    HttpUrl,
    PositiveInt,
    validate_arguments,
    validator,
)

from gpn_clients.utils.patterns import singleton

DEFAULT_HTTP_PORT = 443


@singleton
class NSIConfig(BaseModel):
    HOST: HttpUrl = Field(
        default="https://test-nsi-host.com",
        description="NSI API host",
        alias="host",
    )
    PORT: PositiveInt = Field(
        default=DEFAULT_HTTP_PORT,
        description="NSI API port",
        alias="port",
    )
    API_VERSION: str = Field(
        default="v1",
        alias="api_version",
        description="NSI API version",
        regex="v[0-9]+",
    )

    @classmethod
    @validator("host")
    def drop_last_slash(cls, host: str) -> str:
        if host.endswith("/"):
            return host[:-1]
        return host

    @validate_arguments
    def set_config(
        self,
        host: Optional[Union[HttpUrl, str]] = None,
        port: Optional[Union[PositiveInt, int]] = None,
        api_version: Optional[str] = None,
    ) -> None:
        self.HOST = host or self.HOST
        self.PORT = port or self.PORT
        self.API_VERSION = api_version or self.API_VERSION


nsi_config: NSIConfig = NSIConfig()
