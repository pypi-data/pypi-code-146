from dataclasses import dataclass

from semantha_sdk.model import SemanthaModelEntity


@dataclass(frozen=True)
class Entity(SemanthaModelEntity):

    def __post_init__(self):
        assert type(self.data) is dict

    @property
    def id(self) -> str:
        return str(self.data["id"])

    @property
    def name(self) -> str:
        return str(self.data["name"])
