from typing import Optional

import attrs

from tecton_core import id_helper
from tecton_core.specs import utils
from tecton_proto.common import framework_version_pb2
from tecton_proto.common import id_pb2


__all__ = [
    "TectonObjectSpec",
]


@utils.frozen_strict
class TectonObjectSpec:
    """Base class for all Tecton object (aka First Class Objects or FCO) specs.

    Specs provide a unified, frozen (i.e. immutable), and more useful abstraction over args and data protos for use
    within the Python SDK.

    See the RFC;
    https://www.notion.so/tecton/RFC-Unified-SDK-for-Notebook-Driven-Development-a377af9d320f46488ea238e51e2ce656
    """

    name: str
    id: str
    framework_version: framework_version_pb2.FrameworkVersion.ValueType

    # True if this spec represents an object that was defined locally, as opposed to an "applied" object definition
    # retrieved from the backend.
    is_local_object: bool = attrs.field(metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True})
    workspace: Optional[str] = attrs.field(metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True})

    @property
    def id_proto(self) -> id_pb2.Id:
        return id_helper.IdHelper.from_string(self.id)
