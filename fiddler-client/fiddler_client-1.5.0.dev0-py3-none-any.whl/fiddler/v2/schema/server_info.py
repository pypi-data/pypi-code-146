from pydantic import BaseModel
from typing import Dict, Optional
from semver import VersionInfo


class Version(VersionInfo):

    @classmethod
    def __get_validators__(cls):
        """Return a list of validator methods for pydantic models."""
        yield cls.parse


class ServerInfo(BaseModel):
    features: Dict
    server_version: Optional[Version]
