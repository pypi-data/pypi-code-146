from typing import Optional

import attrs
from typeguard import typechecked

from tecton_core import id_helper
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
            name=utils.get_field_or_none(proto.fco_metadata, "name"),
            id=id_helper.IdHelper.to_string(proto.feature_service_id),
            framework_version=utils.get_field_or_none(proto.fco_metadata, "framework_version"),
            is_local_object=False,
            workspace=utils.get_field_or_none(proto.fco_metadata, "workspace"),
            data_proto=proto,
        )
