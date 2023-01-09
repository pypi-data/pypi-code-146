import enum
from typing import Optional
from typing import Tuple
from typing import Union

import attrs
import pendulum
from typeguard import typechecked

from tecton_core import id_helper
from tecton_core import schema
from tecton_core import time_utils
from tecton_core.specs import tecton_object_spec
from tecton_core.specs import utils
from tecton_proto.args import feature_view_pb2 as feature_view__args_pb2
from tecton_proto.args import pipeline_pb2
from tecton_proto.common import data_source_type_pb2
from tecton_proto.data import feature_store_pb2
from tecton_proto.data import feature_view_pb2 as feature_view__data_pb2


__all__ = [
    "FeatureViewSpec",
    "MaterializedFeatureViewSpec",
    "OnDemandFeatureViewSpec",
    "FeatureTableSpec",
    "MaterializedFeatureViewType",
    "create_feature_view_spec_from_data_proto",
]


@utils.frozen_strict
class FeatureViewSpec(tecton_object_spec.TectonObjectSpec):
    """Base class for feature view specs."""

    join_keys: Tuple[str, ...]
    online_serving_keys: Tuple[str, ...]  # Aka the Online Serving Index.
    feature_store_format_version: feature_store_pb2.FeatureStoreFormatVersion.ValueType = attrs.field()
    view_schema: schema.Schema
    materialization_schema: schema.Schema

    # TODO(TEC-12321): Audit and fix feature view spec fields that should be required.
    offline_store: Optional[feature_view__args_pb2.OfflineFeatureStoreConfig]

    # materialization_enabled is True if the feature view has online or online set to True, and the feature view is
    # applied to a live workspace.
    materialization_enabled: bool
    online: bool
    offline: bool
    materialized_data_path: Optional[str]
    time_range_policy: Optional[feature_view__data_pb2.MaterializationTimeRangePolicy.ValueType]

    # Temporarily expose the underlying data proto during migration.
    # TODO(TEC-12443): Remove this attribute.
    data_proto: Optional[feature_view__data_pb2.FeatureView] = attrs.field(
        metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True}
    )

    @feature_store_format_version.validator
    def check_valid_feature_store_format_version(self, _, value):
        if (
            value < feature_store_pb2.FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_DEFAULT
            or value > feature_store_pb2.FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_MAX
        ):
            raise ValueError(f"Unsupported feature_store_format_version: {value}")


class MaterializedFeatureViewType(enum.Enum):
    TEMPORAL = 1
    TEMPORAL_AGGREGATE = 2


@utils.frozen_strict
class MaterializedFeatureViewSpec(FeatureViewSpec):
    """Spec for Batch and Stream feature views."""

    is_continuous: bool
    type: MaterializedFeatureViewType
    data_source_type: data_source_type_pb2.DataSourceType.ValueType
    incremental_backfills: bool
    timestamp_field: str

    # TODO(TEC-12321): Audit and fix feature view spec fields that should be required.
    pipeline: Optional[pipeline_pb2.Pipeline]

    batch_schedule: Optional[pendulum.Duration]
    slide_interval: Optional[pendulum.Duration]
    ttl: Optional[pendulum.Duration]
    feature_start_time: Optional[pendulum.DateTime]
    materialization_start_time: Optional[pendulum.DateTime]
    max_source_data_delay: pendulum.Duration

    # Generally, data protos should not be exposed in the "spec". However, we make an exception in this case because
    # (a) there is no equivalent args proto, (b) it's a good data model for this usage, and (c) this proto is used
    # extensively in the query gen code (not worth refactoring).
    aggregate_features: Tuple[feature_view__data_pb2.AggregateFeature, ...]
    slide_interval_string: Optional[str]

    # Only relevant for offline-materialized fvs on snowflake compute
    snowflake_view_name: Optional[str]

    # TODO(TEC-12321): Audit and fix feature view spec fields that should be required. (batch_cluster_config should be.)
    batch_cluster_config: Optional[feature_view__args_pb2.ClusterConfig]

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: feature_view__data_pb2.FeatureView) -> "MaterializedFeatureViewSpec":
        batch_schedule = None
        if proto.materialization_params.HasField("schedule_interval"):
            batch_schedule = time_utils.proto_to_duration(proto.materialization_params.schedule_interval)

        feature_start_time = None
        if proto.materialization_params.HasField("feature_start_timestamp"):
            feature_start_time = pendulum.instance(proto.materialization_params.feature_start_timestamp.ToDatetime())

        materialization_start_time = None
        if proto.materialization_params.HasField("materialization_start_timestamp"):
            materialization_start_time = pendulum.instance(
                proto.materialization_params.materialization_start_timestamp.ToDatetime()
            )

        max_source_data_delay = time_utils.proto_to_duration(proto.materialization_params.allowed_upstream_lateness)
        materialized_data_path = utils.get_field_or_none(
            proto.enrichments.fp_materialization.materialized_data_location, "path"
        )

        snowflake_view_name = None
        if proto.HasField("snowflake_data"):
            snowflake_view_name = utils.get_field_or_none(proto.snowflake_data, "snowflake_view_name")

        if proto.HasField("temporal_aggregate"):
            assert proto.temporal_aggregate.HasField("slide_interval")

            return cls(
                name=utils.get_field_or_none(proto.fco_metadata, "name"),
                id=id_helper.IdHelper.to_string(proto.feature_view_id),
                join_keys=utils.get_tuple_from_repeated_field(proto.join_keys),
                online_serving_keys=utils.get_tuple_from_repeated_field(proto.online_serving_index.join_keys),
                framework_version=utils.get_field_or_none(proto.fco_metadata, "framework_version"),
                view_schema=_get_view_schema(proto.schemas),
                materialization_schema=_get_materialization_schema(proto.schemas),
                is_local_object=False,
                workspace=utils.get_field_or_none(proto.fco_metadata, "workspace"),
                offline_store=utils.get_field_or_none(proto.materialization_params, "offline_store_config"),
                is_continuous=proto.temporal_aggregate.is_continuous,
                data_source_type=utils.get_field_or_none(proto.temporal_aggregate, "data_source_type"),
                incremental_backfills=False,
                timestamp_field=utils.get_field_or_none(proto, "timestamp_key"),
                type=MaterializedFeatureViewType.TEMPORAL_AGGREGATE,
                feature_store_format_version=proto.feature_store_format_version,
                materialization_enabled=proto.materialization_enabled,
                online=proto.materialization_params.writes_to_online_store,
                offline=proto.materialization_params.writes_to_offline_store,
                pipeline=utils.get_field_or_none(proto, "pipeline"),
                batch_schedule=batch_schedule,
                slide_interval=time_utils.proto_to_duration(proto.temporal_aggregate.slide_interval),
                ttl=None,
                feature_start_time=feature_start_time,
                materialization_start_time=materialization_start_time,
                max_source_data_delay=max_source_data_delay,
                aggregate_features=utils.get_tuple_from_repeated_field(proto.temporal_aggregate.features),
                slide_interval_string=utils.get_field_or_none(proto.temporal_aggregate, "slide_interval_string"),
                materialized_data_path=materialized_data_path,
                time_range_policy=utils.get_field_or_none(proto.materialization_params, "time_range_policy"),
                snowflake_view_name=snowflake_view_name,
                data_proto=proto,
                batch_cluster_config=utils.get_field_or_none(proto.materialization_params, "batch_materialization"),
            )
        elif proto.HasField("temporal"):
            assert proto.temporal.HasField("serving_ttl")

            return cls(
                name=utils.get_field_or_none(proto.fco_metadata, "name"),
                id=id_helper.IdHelper.to_string(proto.feature_view_id),
                join_keys=utils.get_tuple_from_repeated_field(proto.join_keys),
                online_serving_keys=utils.get_tuple_from_repeated_field(proto.online_serving_index.join_keys),
                framework_version=utils.get_field_or_none(proto.fco_metadata, "framework_version"),
                view_schema=_get_view_schema(proto.schemas),
                materialization_schema=_get_materialization_schema(proto.schemas),
                is_local_object=False,
                workspace=utils.get_field_or_none(proto.fco_metadata, "workspace"),
                offline_store=utils.get_field_or_none(proto.materialization_params, "offline_store_config"),
                is_continuous=proto.temporal.is_continuous,
                data_source_type=utils.get_field_or_none(proto.temporal, "data_source_type"),
                incremental_backfills=proto.temporal.incremental_backfills,
                timestamp_field=utils.get_field_or_none(proto, "timestamp_key"),
                type=MaterializedFeatureViewType.TEMPORAL,
                feature_store_format_version=proto.feature_store_format_version,
                materialization_enabled=proto.materialization_enabled,
                online=proto.materialization_params.writes_to_online_store,
                offline=proto.materialization_params.writes_to_offline_store,
                pipeline=utils.get_field_or_none(proto, "pipeline"),
                batch_schedule=batch_schedule,
                slide_interval=None,
                ttl=time_utils.proto_to_duration(proto.temporal.serving_ttl),
                feature_start_time=feature_start_time,
                materialization_start_time=materialization_start_time,
                max_source_data_delay=max_source_data_delay,
                aggregate_features=tuple(),
                slide_interval_string=None,
                materialized_data_path=materialized_data_path,
                time_range_policy=utils.get_field_or_none(proto.materialization_params, "time_range_policy"),
                snowflake_view_name=snowflake_view_name,
                data_proto=proto,
                batch_cluster_config=utils.get_field_or_none(proto.materialization_params, "batch_materialization"),
            )
        else:
            raise TypeError(f"Unexpected feature view type: {proto}")


@utils.frozen_strict
class OnDemandFeatureViewSpec(FeatureViewSpec):
    # TODO(TEC-12321): Audit and fix feature view spec fields that should be required.
    pipeline: Optional[pipeline_pb2.Pipeline]

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: feature_view__data_pb2.FeatureView) -> "OnDemandFeatureViewSpec":
        return cls(
            name=utils.get_field_or_none(proto.fco_metadata, "name"),
            id=id_helper.IdHelper.to_string(proto.feature_view_id),
            join_keys=utils.get_tuple_from_repeated_field(proto.join_keys),
            online_serving_keys=utils.get_tuple_from_repeated_field(proto.online_serving_index.join_keys),
            framework_version=utils.get_field_or_none(proto.fco_metadata, "framework_version"),
            view_schema=_get_view_schema(proto.schemas),
            materialization_schema=_get_materialization_schema(proto.schemas),
            is_local_object=False,
            workspace=utils.get_field_or_none(proto.fco_metadata, "workspace"),
            offline_store=utils.get_field_or_none(proto.materialization_params, "offline_store_config"),
            feature_store_format_version=proto.feature_store_format_version,
            materialization_enabled=False,
            online=False,
            offline=False,
            pipeline=utils.get_field_or_none(proto, "pipeline"),
            materialized_data_path=None,
            time_range_policy=utils.get_field_or_none(proto.materialization_params, "time_range_policy"),
            data_proto=proto,
        )


@utils.frozen_strict
class FeatureTableSpec(FeatureViewSpec):
    timestamp_field: str
    ttl: pendulum.Duration

    # TODO(TEC-12321): Audit and fix feature view spec fields that should be required. (batch_cluster_config should be.)
    batch_cluster_config: Optional[feature_view__args_pb2.ClusterConfig]

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: feature_view__data_pb2.FeatureView) -> "FeatureTableSpec":
        ttl = None
        if proto.feature_table.HasField("serving_ttl"):
            ttl = time_utils.proto_to_duration(proto.feature_table.serving_ttl)

        materialized_data_path = utils.get_field_or_none(
            proto.enrichments.fp_materialization.materialized_data_location, "path"
        )

        return cls(
            name=utils.get_field_or_none(proto.fco_metadata, "name"),
            id=id_helper.IdHelper.to_string(proto.feature_view_id),
            join_keys=utils.get_tuple_from_repeated_field(proto.join_keys),
            online_serving_keys=utils.get_tuple_from_repeated_field(proto.online_serving_index.join_keys),
            framework_version=utils.get_field_or_none(proto.fco_metadata, "framework_version"),
            view_schema=_get_view_schema(proto.schemas),
            materialization_schema=_get_materialization_schema(proto.schemas),
            is_local_object=False,
            workspace=utils.get_field_or_none(proto.fco_metadata, "workspace"),
            offline_store=utils.get_field_or_none(proto.materialization_params, "offline_store_config"),
            timestamp_field=utils.get_field_or_none(proto, "timestamp_key"),
            feature_store_format_version=proto.feature_store_format_version,
            materialization_enabled=proto.materialization_enabled,
            online=proto.feature_table.online_enabled,
            offline=proto.feature_table.offline_enabled,
            ttl=ttl,
            materialized_data_path=materialized_data_path,
            time_range_policy=utils.get_field_or_none(proto.materialization_params, "time_range_policy"),
            data_proto=proto,
            batch_cluster_config=utils.get_field_or_none(proto.materialization_params, "batch_materialization"),
        )


def _get_view_schema(schemas: feature_view__data_pb2.FeatureViewSchemas) -> Optional[schema.Schema]:
    if schemas.HasField("view_schema"):
        return schema.Schema(schemas.view_schema)
    else:
        return None


def _get_materialization_schema(schemas: feature_view__data_pb2.FeatureViewSchemas) -> Optional[schema.Schema]:
    if schemas.HasField("materialization_schema"):
        return schema.Schema(schemas.materialization_schema)
    else:
        return None


@typechecked
def create_feature_view_spec_from_data_proto(
    proto: feature_view__data_pb2.FeatureView,
) -> Optional[Union[MaterializedFeatureViewSpec, OnDemandFeatureViewSpec, FeatureTableSpec]]:
    if proto.HasField("temporal_aggregate") or proto.HasField("temporal"):
        return MaterializedFeatureViewSpec.from_data_proto(proto)
    elif proto.HasField("on_demand_feature_view"):
        return OnDemandFeatureViewSpec.from_data_proto(proto)
    elif proto.HasField("feature_table"):
        return FeatureTableSpec.from_data_proto(proto)
    else:
        raise ValueError(f"Unexpect feature view type: {proto}")
