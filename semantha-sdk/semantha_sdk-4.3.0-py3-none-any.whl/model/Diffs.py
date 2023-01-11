from __future__ import annotations

from dataclasses import dataclass

from semantha_sdk.model import SemanthaModelEntity


@dataclass(frozen=True)
class Diff(SemanthaModelEntity):

    def __post_init__(self):
        assert type(self.data) is dict

    @property
    def operation(self) -> str:
        return str(self.data["operation"])

    @property
    def text(self) -> str:
        return str(self.data["text"])


@dataclass(frozen=True)
class Diffs(SemanthaModelEntity):

    def __post_init__(self):
        assert type(self.data) is list

    @property
    def diffs(self) -> list[Diff]:
        return [Diff(raw_diff) for raw_diff in self.data]
