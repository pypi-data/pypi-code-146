from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from semantha_sdk.model import SemanthaModelEntity


@dataclass(frozen=True)
class Synonym(SemanthaModelEntity):

    def __post_init__(self):
        assert type(self.data) is dict

    @property
    def id(self) -> str:
        return str(self.data["id"])

    @property
    def word(self) -> Optional[str]:
        if self.data.get("word"):
            return self.data["word"]

    @property
    def regex(self) -> Optional[str]:
        if self.data.get("regex"):
            return self.data["regex"]

    @property
    def synonym(self) -> str:
        return self.data["synonym"]

    @property
    def tags(self) -> list[str]:
        return self.data.get("tags")


@dataclass(frozen=True)
class Synonyms(SemanthaModelEntity):

    def __post_init__(self):
        assert type(self.data) is list

    @property
    def synonyms(self) -> list[Synonym]:
        return [Synonym(raw_synonym) for raw_synonym in self.data]
