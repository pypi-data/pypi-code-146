from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from semantha_sdk.model import SemanthaModelEntity, Reference


@dataclass(frozen=True)
class Sentence(SemanthaModelEntity):

    def __post_init__(self):
        assert type(self.data) is dict

    @property
    def id(self) -> str:
        return self.data["id"]

    @property
    def text(self) -> str:
        return self.data["text"]

    @property
    def document_name(self) -> Optional[str]:
        return None

    @property
    def named_entities(self):
        return None

    @property
    def references(self) -> Optional[list[Reference]]:
        return [
            Reference(raw_reference)
            for raw_reference in self.data.get("references", [])
        ]

    @property
    def areas(self):
        return None
