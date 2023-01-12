from __future__ import annotations
from enum import Enum


class PublicConfigOutput(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def versions(self) -> list["VersionOutput"]:
        return [VersionOutput(**version) for version in self["versions"]]


class VersionOutput(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def version(self) -> str:
        return str(self["version"])

    @property
    def artifact_name(self) -> "ArtifactName":
        return ArtifactName(self["artifactName"])


class ArtifactName(Enum):
    GLOBAL = "GLOBAL"
    BACKEND = "BACKEND"
