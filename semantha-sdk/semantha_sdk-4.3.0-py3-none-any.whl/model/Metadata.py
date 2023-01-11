from dataclasses import dataclass

from semantha_sdk.model import SemanthaModelEntity


@dataclass(frozen=True)
class Metadata(SemanthaModelEntity):

    def __post_init__(self):
        assert type(self.data) is dict
        assert "id" in self.data.keys() and "value" in self.data.keys()
        assert type(self.data["id"]) is str and type(self.data["value"]) is str
