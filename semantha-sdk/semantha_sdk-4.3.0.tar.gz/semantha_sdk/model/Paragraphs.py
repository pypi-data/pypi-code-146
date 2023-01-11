from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from semantha_sdk.model import Reference, SemanthaModelEntity
from semantha_sdk.model.Sentences import Sentence


@dataclass(frozen=True)
class Paragraph(SemanthaModelEntity):

    def __post_init__(self):
        assert type(self.data) is dict

    @property
    def id(self) -> str:
        return self.data["id"]

    @property
    def type(self) -> str:
        return self.data["type"]

    @property
    def text(self) -> str:
        return self.data["text"]

    @property
    def sentences(self) -> list[Sentence]:
        return [
            Sentence(raw_sentence) for raw_sentence in self.data["sentences"]
        ]

    @property
    def document_name(self) -> Optional[str]:
        # TODO IDK if that name is correct
        return (
            self.data["documentName"]
            if "documentName" in self.data
            else None
        )

    @property
    def references(self) -> Optional[list[Reference]]:
        return [
            Reference(raw_sentence)
            for raw_sentence in self.data.get("references", [])
        ]

    @property
    def context(self) -> dict[str, str]:
        return None

    @property
    def area(self):
        return None

    @property
    def comment(self) -> str:
        return None

    @property
    def data_url_imag(self) -> str:
        return None

    context: dict[str, str] = None
    # TODO: areas DTO
    areas = None
    comment: str = None
    data_url_imag: str = None

    # TODO: error handling
    # TODO: type hints
