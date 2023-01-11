from __future__ import annotations

from dataclasses import dataclass

from semantha_sdk.model import SemanthaModelEntity


@dataclass(frozen=True)
class ClusteredDocument(SemanthaModelEntity):

    def __post_init__(self):
        assert type(self.data) is dict

    @property
    def document_id(self) -> str:
        return str(self.data["documentId"])

    @property
    def probability(self) -> float:
        return float(self.data["probability"])


@dataclass(frozen=True)
class ClusteredParagraph(SemanthaModelEntity):

    def __post_init__(self):
        assert type(self.data) is dict

    @property
    def document_id(self) -> str:
        return str(self.data["documentId"])

    @property
    def paragraph_id(self) -> str:
        return str(self.data["paragraphId"])

    @property
    def probability(self) -> float:
        return float(self.data["probability"])


@dataclass(frozen=True)
class DocumentCluster(SemanthaModelEntity):

    def __post_init__(self):
        assert type(self.data) is dict

    @property
    def id(self) -> int:
        return int(self.data["id"])

    @property
    def count(self) -> int:
        return int(self.data["count"])

    @property
    def label(self) -> str:
        return str(self.data["label"])

    @property
    def content(self) -> list[ClusteredDocument]:
        return [
            ClusteredDocument(raw_doc) for raw_doc in self.data["content"]
        ]


@dataclass(frozen=True)
class ParagraphCluster(SemanthaModelEntity):

    def __post_init__(self):
        assert type(self.data) is dict

    @property
    def id(self) -> int:
        return int(self.data["id"])

    @property
    def count(self) -> int:
        return int(self.data["count"])

    @property
    def label(self) -> str:
        return str(self.data["label"])

    @property
    def content(self) -> list[ClusteredParagraph]:
        return [
            ClusteredParagraph(raw_doc) for raw_doc in self.data["content"]
        ]


@dataclass(frozen=True)
class DocumentClusters(SemanthaModelEntity):

    def __post_init__(self):
        assert type(self.data) is list

    @property
    def clusters(self) -> list[DocumentCluster]:
        return [DocumentCluster(raw_doc_cluster) for raw_doc_cluster in self.data]


@dataclass(frozen=True)
class ParagraphClusters(SemanthaModelEntity):

    def __post_init__(self):
        assert type(self.data) is list

    @property
    def clusters(self) -> list[ParagraphCluster]:
        return [ParagraphCluster(raw_para_cluster) for raw_para_cluster in self.data]
