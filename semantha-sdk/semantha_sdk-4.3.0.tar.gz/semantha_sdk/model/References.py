from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from semantha_sdk.model import SemanthaModelEntity


@dataclass(frozen=True)
class Reference(SemanthaModelEntity):

    def __post_init__(self):
        assert type(self.data) is dict

    @property
    def document_id(self) -> str:
        return self.data["documentId"]
        pass

    @property
    def similarity(self) -> float:
        return float(self.data["similarity"])

    @property
    def color(self) -> str:
        return self.data["color"]

    @property
    def document_name(self) -> Optional[str]:
        return self.data.get("documentName", None)

    def page_numer(self) -> Optional[int]:
        return (
            int(self.data["pageNumber"])
            if "pageNumber" in self.data
            else None
        )

    @property
    def paragraph_id(self) -> Optional[str]:
        return self.data.get("paragraphId", None)

    @property
    def sentence_id(self) -> Optional[str]:
        return self.data.get("sentenceId", None)

    @property
    def text(self) -> Optional[str]:
        return self.data.get("text", None)

    @property
    def context(self) -> Optional[dict[str, str]]:
        return self.data.get("context", None)

    @property
    def type(self) -> Optional[str]:
        return self.data.get("type", None)

    @property
    def comment(self) -> Optional[str]:
        return self.data.get("comment", None)

    @property
    def has_opposite_meaning(self) -> Optional[bool]:
        return (
            bool(self.data.get("hasOppositeMeaning", None))
            if "hasOppositeMeaning" in self.data
            else None
        )
