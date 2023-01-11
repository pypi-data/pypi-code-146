from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from semantha_sdk.model import Reference, Page, SemanthaModelEntity
from semantha_sdk.model.ReferenceDocuments import DocumentInformation


@dataclass(frozen=True)
class Document(DocumentInformation):

    def __post_init__(self):
        assert type(self.data) is dict

    @property
    def pages(self) -> list[Page]:
        return [Page(raw_page) for raw_page in self.data["pages"]]

    @property
    def references(self) -> Optional[list[Reference]]:
        return [
            Reference(raw_reference)
            for raw_reference in self.data.get("references", [])
        ]

    @property
    def image_pages(self) -> Optional[str]:
        return None


@dataclass(frozen=True)
class Documents(SemanthaModelEntity):

    def __post_init__(self):
        assert type(self.data) is list

    @property
    def documents(self) -> list[Document]:
        return [Document(raw_document) for raw_document in self.data]
