from dataclasses import dataclass

from semantha_sdk.model import SemanthaModelEntity


@dataclass(frozen=True)
class NamedEntity(SemanthaModelEntity):

    def __post_init__(self):
        assert type(self.data) is dict

    @property
    def name(self):
        return str(self.data["name"])

    @property
    def text(self):
        return str(self.data["text"])


@dataclass(frozen=True)
class NamedEntities(SemanthaModelEntity):

    def __post_init__(self):
        assert type(self.data) is list

    def __getitem__(self, index) -> NamedEntity:
        return NamedEntity(self.data[index])
