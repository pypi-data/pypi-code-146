from dataclasses import dataclass

from semantha_sdk.model import SemanthaModelEntity


@dataclass(frozen=True)
class Label(SemanthaModelEntity):

    def __post_init__(self):
        assert type(self.data) is dict
        assert type(self.data["lang"]) is str and type(self.data["value"]) is str
