from __future__ import annotations

import datetime
from typing import Dict
from typing import Optional

import attrs
from typeguard import typechecked

from tecton_core import id_helper
from tecton_core import specs
from tecton_proto.args import basic_info_pb2
from tecton_proto.args import fco_args_pb2
from tecton_proto.args import repo_metadata_pb2
from tecton_proto.common import id_pb2


@attrs.frozen
class TectonObjectInfo:
    """A public SDK dataclass containing common metadata used for all Tecton Objects."""

    id: str
    name: str
    description: Optional[str]
    tags: Dict[str, str]
    owner: Optional[str]
    created_at: Optional[datetime.datetime]
    workspace: Optional[str]

    @classmethod
    @typechecked
    def from_args_proto(cls, basic_info: basic_info_pb2.BasicInfo, id: id_pb2.Id) -> TectonObjectInfo:
        return cls(
            id=id_helper.IdHelper.to_string(id),
            name=basic_info.name,
            description=basic_info.description if basic_info.HasField("description") else None,
            tags=dict(basic_info.tags),
            owner=basic_info.owner if basic_info.HasField("owner") else None,
            created_at=None,  # created_at is only filled for remote (i.e. applied) Tecton objects.
            workspace=None,  # workspace is only filled for remote (i.e. applied) Tecton objects.
        )

    @classmethod
    @typechecked
    def from_spec(cls, spec: specs.TectonObjectSpec) -> TectonObjectInfo:
        return cls(
            id=spec.id,
            name=spec.name,
            description=spec.metadata.description,
            tags=spec.metadata.tags,
            owner=spec.metadata.owner,
            created_at=spec.metadata.created_at,
            workspace=spec.workspace,
        )

    @property
    def _id_proto(self) -> id_pb2.Id:
        return id_helper.IdHelper.from_string(self.id)


@attrs.define
class BaseTectonObject:
    """A base dataclass for all public FCO classes to inherit from.

    Attributes:
        info: A dataclass containing basic info about this Tecton Object.
        _source_info: Metadata about where this object was defined in the repo, e.g. the filename and line number. Only
            set if this object was defined locally.
    """

    info: TectonObjectInfo = attrs.field(on_setattr=attrs.setters.frozen)
    _source_info: Optional[repo_metadata_pb2.SourceInfo] = attrs.field(repr=False, on_setattr=attrs.setters.frozen)

    @property
    def _is_valid(self):
        raise NotImplementedError

    def validate(self):
        raise NotImplementedError

    def _build_args(self) -> fco_args_pb2.FcoArgs:
        """Returns a copy of the args as a FcoArgs proto for plan/apply logic."""
        raise NotImplementedError
