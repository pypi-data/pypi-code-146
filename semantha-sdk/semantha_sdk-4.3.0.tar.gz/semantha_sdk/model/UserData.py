from __future__ import annotations

from dataclasses import dataclass

from semantha_sdk.model import SemanthaModelEntity


@dataclass(frozen=True)
class UserData(SemanthaModelEntity):

    def __post_init__(self):
        assert type(self.data) is dict

    @property
    def name(self) -> str:
        return str(self.data["name"])

    @property
    def valid_until(self) -> int:
        return int(self.data["validUntil"])

    @property
    def roles(self) -> list[str]:
        return self.data['roles']
