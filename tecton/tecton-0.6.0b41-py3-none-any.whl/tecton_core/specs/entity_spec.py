from typing import Optional
from typing import Tuple

import attrs
from typeguard import typechecked

from tecton_core.specs import tecton_object_spec
from tecton_core.specs import utils
from tecton_proto.args import entity_pb2 as entity__args_pb2
from tecton_proto.data import entity_pb2 as entity__data_pb2

__all__ = [
    "EntitySpec",
]


@utils.frozen_strict
class EntitySpec(tecton_object_spec.TectonObjectSpec):
    join_keys: Tuple[str, ...]

    # Temporarily expose the underlying data proto during migration.
    # TODO(TEC-12443): Remove this attribute.
    data_proto: Optional[entity__data_pb2.Entity] = attrs.field(metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True})

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: entity__data_pb2.Entity) -> "EntitySpec":
        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_data_proto(proto.entity_id, proto.fco_metadata),
            join_keys=utils.get_tuple_from_repeated_field(proto.join_keys),
            data_proto=proto,
        )

    @classmethod
    @typechecked
    def from_args_proto(cls, proto: entity__args_pb2.EntityArgs) -> "EntitySpec":
        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_args_proto(proto.entity_id, proto.info),
            join_keys=utils.get_tuple_from_repeated_field(proto.join_keys),
            data_proto=None,
        )
