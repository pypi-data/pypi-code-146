from dataclasses import dataclass

from semantha_sdk.model import SemanthaModelEntity
from semantha_sdk.model.DomainSettings import DomainSettings


@dataclass(frozen=True)
class DomainConfiguration(SemanthaModelEntity):

    def __post_init__(self):
        assert type(self.data) is dict

    @property
    def id(self) -> str:
        return str(self.data["id"])

    @property
    def name(self) -> str:
        return str(self.data["name"])

    @property
    def settings(self) -> DomainSettings:
        return DomainSettings(self.data["settings"])
