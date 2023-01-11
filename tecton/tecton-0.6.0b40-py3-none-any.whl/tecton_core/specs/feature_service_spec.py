from typing import Optional

import attrs
from typeguard import typechecked

from tecton_core.specs import tecton_object_spec
from tecton_core.specs import utils
from tecton_proto.data import feature_service_pb2 as feature_service__data_pb2

__all__ = [
    "FeatureServiceSpec",
]


@utils.frozen_strict
class FeatureServiceSpec(tecton_object_spec.TectonObjectSpec):
    # Temporarily expose the underlying data proto during migration.
    # TODO(TEC-12443): Remove this attribute.
    data_proto: Optional[feature_service__data_pb2.FeatureService] = attrs.field(
        metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True}
    )

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: feature_service__data_pb2.FeatureService) -> "FeatureServiceSpec":
        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_data_proto(
                proto.feature_service_id, proto.fco_metadata
            ),
            data_proto=proto,
        )
