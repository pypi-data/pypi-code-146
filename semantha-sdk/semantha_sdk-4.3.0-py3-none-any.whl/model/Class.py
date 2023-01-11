from __future__ import annotations

from dataclasses import dataclass

from semantha_sdk.model import SemanthaModelEntity, Label, Metadata, DataType


@dataclass(frozen=True)
class Class(SemanthaModelEntity):

    def __post_init__(self):
        assert type(self.data["id"]) is str
        assert type(self.data["name"]) is str
        assert type(self.data["readOnly"]) is bool
        assert type(self.data["functional"]) is bool
        assert type(self.data["labels"]) is list[dict]
        assert type(self.data["metadata"]) is list[dict]
        assert type(self.data["comment"]) is str
        assert self.data["datatype"] in DataType.list()
        assert type(self.data["attributeIds"]) is list[str]
        assert type(self.data["relevantForRelation"]) is bool
        assert type(self.data["objectPropertyId"]) is str
        assert type(self.data["parentId"]) is str

    @property
    def labels(self) -> list[Label]:
        return [
            Label(label)
            for label in self.data.get("labels", [])
        ]

    @property
    def metadata(self) -> list[Metadata]:
        return [
            Metadata(values) for values in self.data.get("metadata", [])
        ]
