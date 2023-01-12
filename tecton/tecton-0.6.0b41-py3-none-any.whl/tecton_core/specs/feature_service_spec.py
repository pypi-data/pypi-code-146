from typing import Optional
from typing import Tuple

import attrs
from typeguard import typechecked

from tecton_core import id_helper
from tecton_core.specs import tecton_object_spec
from tecton_core.specs import utils
from tecton_proto.data import feature_service_pb2 as feature_service__data_pb2

__all__ = [
    "FeatureServiceSpec",
    "FeatureSetItemSpec",
]


@utils.frozen_strict
class FeatureServiceSpec(tecton_object_spec.TectonObjectSpec):
    feature_set_items: Tuple["FeatureSetItemSpec", ...]
    online_serving_enabled: bool

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
            feature_set_items=tuple(FeatureSetItemSpec.from_data_proto(item) for item in proto.feature_set_items),
            online_serving_enabled=proto.online_serving_enabled,
            data_proto=proto,
        )


@utils.frozen_strict
class FeatureSetItemSpec:
    feature_view_id: str
    namespace: str
    feature_columns: Tuple[str, ...]
    # Mapping from spine join key to the Feature View join keys.  Not a dict to account for multi-mapping.
    join_key_mappings: Tuple["JoinKeyMappingSpec", ...]

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: feature_service__data_pb2.FeatureSetItem) -> "FeatureSetItemSpec":
        join_key_mappings = []
        for join_configuration_item in proto.join_configuration_items:
            join_key_mappings.append(
                JoinKeyMappingSpec(
                    spine_column_name=join_configuration_item.spine_column_name,
                    feature_view_column_name=join_configuration_item.package_column_name,
                )
            )

        return cls(
            feature_view_id=id_helper.IdHelper.to_string(proto.feature_view_id),
            namespace=utils.get_field_or_none(proto, "namespace"),
            feature_columns=utils.get_tuple_from_repeated_field(proto.feature_columns),
            join_key_mappings=tuple(join_key_mappings),
        )


@utils.frozen_strict
class JoinKeyMappingSpec:
    spine_column_name: str
    feature_view_column_name: str


# Resolve forward type declarations.
attrs.resolve_types(FeatureServiceSpec, locals(), globals())
attrs.resolve_types(FeatureSetItemSpec, locals(), globals())
