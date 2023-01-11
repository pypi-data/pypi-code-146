from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from semantha_sdk.model import SemanthaModelEntity
from semantha_sdk.model.Entity import Entity


@dataclass(frozen=True)
class Parameters(SemanthaModelEntity):
    # TODO: add remaining information whhich is created if we use sorting, filtering or return fields
    #       in reference documents get_all()

    def __post_init__(self):
        assert type(self.data) is dict

    @property
    def domain(self) -> str:
        return str(self.data["domain"])


@dataclass(frozen=True)
class Meta(SemanthaModelEntity):

    def __post_init__(self):
        assert type(self.data) is dict

    @property
    def parameters(self) -> Parameters:
        return Parameters(self.data["parameters"])


@dataclass(frozen=True)
class DocumentInformation(SemanthaModelEntity):
    # TODO: make all (?) properties optional since they might not be present if we use return fields parameter in
    #       reference documents get_all()

    def __post_init__(self):
        assert type(self.data) is dict

    @property
    def id(self) -> str:
        return str(self.data["id"])

    @property
    def name(self) -> str:
        return str(self.data["name"])

    @property
    def tags(self) -> list[str]:
        return self.data["tags"]

    @property
    def metadata(self) -> str:
        return str(self.data["metadata"])

    @property
    def filename(self) -> str:
        return str(self.data["filename"])

    @property
    def created(self) -> int:
        return int(self.data["created"])

    @property
    def updated(self) -> int:
        return int(self.data["updated"])

    @property
    def processed(self) -> int:
        return bool(self.data["processed"])

    @property
    def lang(self) -> Optional[str]:
        return self.data.get("documentName", None)

    @property
    def content(self) -> Optional[str]:
        return self.data.get("content", None)

    @property
    def document_class(self) -> Optional[Entity]:
        return self.data.get("documentClass", None)

    @property
    def derived_tags(self) -> list[str]:
        return self.data["derivedTags"]

    @property
    def color(self) -> Optional[str]:
        return self.data.get("color", None)

    @property
    def derived_color(self) -> Optional[str]:
        return self.data.get("derivedColor", None)

    @property
    def comment(self) -> Optional[str]:
        return self.data.get("comment", None)

    @property
    def derived_comment(self) -> Optional[str]:
        return self.data.get("derivedComment", None)


@dataclass(frozen=True)
class _DocsPerTag(SemanthaModelEntity):

    def __post_init__(self):
        assert type(self.data) is dict

    @property
    def tag(self) -> str:
        return str(self.data["tag"])

    @property
    def count(self) -> int:
        return int(self.data["count"])


@dataclass(frozen=True)
class Statistic(SemanthaModelEntity):

    def __post_init__(self):
        assert type(self.data) is dict

    @property
    def library_size(self) -> int:
        return int(self.data["librarySize"])

    @property
    def size(self) -> int:
        return int(self.data["size"])

    @property
    def number_of_sentences(self) -> int:
        return int(self.data["numberOfSentences"])

    @property
    def docs_per_tag(self) -> list[_DocsPerTag]:
        return [
            _DocsPerTag(docs_per_tag) for docs_per_tag in self.data["docsPerTag"]
        ]


@dataclass(frozen=True)
class ReferenceDocumentCollection(SemanthaModelEntity):
    def __post_init__(self):
        assert type(self.data) is list

    def __getitem__(self, index):
        return DocumentInformation(self.data[index])


@dataclass(frozen=True)
class ReferenceDocuments(SemanthaModelEntity):

    def __post_init__(self):
        assert type(self.data) is dict

    @property
    def meta(self) -> Meta:
        return Meta(self.data["meta"])

    @property
    def documents(self) -> ReferenceDocumentCollection:
        return ReferenceDocumentCollection(self.data["data"])
