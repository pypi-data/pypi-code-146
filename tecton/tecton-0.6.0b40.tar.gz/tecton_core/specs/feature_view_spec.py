import enum
from typing import Optional
from typing import Tuple
from typing import Union

import attrs
import pendulum
from typeguard import typechecked

from tecton_core import id_helper
from tecton_core import pipeline_common
from tecton_core import schema
from tecton_core import time_utils
from tecton_core.data_types import TimestampType
from tecton_core.specs import tecton_object_spec
from tecton_core.specs import utils
from tecton_proto.args import feature_view_pb2 as feature_view__args_pb2
from tecton_proto.args import pipeline_pb2
from tecton_proto.common import data_source_type_pb2
from tecton_proto.common import schema_pb2
from tecton_proto.data import feature_store_pb2
from tecton_proto.data import feature_view_pb2 as feature_view__data_pb2

__all__ = [
    "FeatureViewSpec",
    "MaterializedFeatureViewSpec",
    "OnDemandFeatureViewSpec",
    "FeatureTableSpec",
    "MaterializedFeatureViewType",
    "create_feature_view_spec_from_data_proto",
    "create_feature_view_spec_from_args_proto",
    "FeatureViewSpecArgsSupplement",
]


@utils.frozen_strict
class FeatureViewSpec(tecton_object_spec.TectonObjectSpec):
    """Base class for feature view specs."""

    join_keys: Tuple[str, ...]
    entity_ids: Tuple[str, ...]
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


@attrs.define
class FeatureViewSpecArgsSupplement:
    """A data class used for supplementing args protos during FeatureViewSpec construction.

    This Python data class can be used to include data that is not included in args protos (e.g. schemas) into the
    FeatureViewSpec constructor.
    """

    view_schema: Optional[schema_pb2.Schema]
    materialization_schema: Optional[schema_pb2.Schema]


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
        if proto.HasField("temporal_aggregate"):
            fv_type = MaterializedFeatureViewType.TEMPORAL_AGGREGATE
            is_continuous = proto.temporal_aggregate.is_continuous
            data_source_type = utils.get_field_or_none(proto.temporal_aggregate, "data_source_type")
            incremental_backfills = False
            slide_interval = time_utils.proto_to_duration(proto.temporal_aggregate.slide_interval)
            ttl = None
            aggregate_features = utils.get_tuple_from_repeated_field(proto.temporal_aggregate.features)
            slide_interval_string = utils.get_field_or_none(proto.temporal_aggregate, "slide_interval_string")
        elif proto.HasField("temporal"):
            fv_type = MaterializedFeatureViewType.TEMPORAL
            is_continuous = proto.temporal.is_continuous
            data_source_type = utils.get_field_or_none(proto.temporal, "data_source_type")
            incremental_backfills = proto.temporal.incremental_backfills
            slide_interval = None
            ttl = time_utils.proto_to_duration(proto.temporal.serving_ttl)
            aggregate_features = tuple()
            slide_interval_string = None
        else:
            raise TypeError(f"Unexpected feature view type: {proto}")

        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_data_proto(
                proto.feature_view_id, proto.fco_metadata
            ),
            entity_ids=tuple(id_helper.IdHelper.to_string(id) for id in proto.entity_ids),
            join_keys=utils.get_tuple_from_repeated_field(proto.join_keys),
            online_serving_keys=utils.get_tuple_from_repeated_field(proto.online_serving_index.join_keys),
            view_schema=_get_view_schema(proto.schemas),
            materialization_schema=_get_materialization_schema(proto.schemas),
            offline_store=utils.get_field_or_none(proto.materialization_params, "offline_store_config"),
            is_continuous=is_continuous,
            data_source_type=data_source_type,
            incremental_backfills=incremental_backfills,
            timestamp_field=utils.get_field_or_none(proto, "timestamp_key"),
            type=fv_type,
            feature_store_format_version=proto.feature_store_format_version,
            materialization_enabled=proto.materialization_enabled,
            online=proto.materialization_params.writes_to_online_store,
            offline=proto.materialization_params.writes_to_offline_store,
            pipeline=utils.get_field_or_none(proto, "pipeline"),
            batch_schedule=utils.get_duration_field_or_none(proto.materialization_params, "schedule_interval"),
            slide_interval=slide_interval,
            ttl=ttl,
            feature_start_time=utils.get_timestamp_field_or_none(
                proto.materialization_params, "feature_start_timestamp"
            ),
            materialization_start_time=utils.get_timestamp_field_or_none(
                proto.materialization_params, "materialization_start_timestamp"
            ),
            max_source_data_delay=time_utils.proto_to_duration(proto.materialization_params.allowed_upstream_lateness),
            aggregate_features=aggregate_features,
            slide_interval_string=slide_interval_string,
            materialized_data_path=utils.get_field_or_none(
                proto.enrichments.fp_materialization.materialized_data_location, "path"
            ),
            time_range_policy=utils.get_field_or_none(proto.materialization_params, "time_range_policy"),
            snowflake_view_name=utils.get_field_or_none(proto.snowflake_data, "snowflake_view_name"),
            data_proto=proto,
            batch_cluster_config=utils.get_field_or_none(proto.materialization_params, "batch_materialization"),
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls, proto: feature_view__args_pb2.FeatureViewArgs, supplement: FeatureViewSpecArgsSupplement
    ) -> "MaterializedFeatureViewSpec":
        entity_ids = []
        join_keys = []
        for entity in proto.entities:
            entity_ids.append(id_helper.IdHelper.to_string(entity.entity_id))
            join_keys.extend(entity.join_keys)

        online_serving_keys = proto.online_serving_index if proto.online_serving_index else join_keys

        is_aggregate = len(proto.materialized_feature_view_args.aggregations) > 0
        if is_aggregate:
            fv_type = MaterializedFeatureViewType.TEMPORAL_AGGREGATE
        else:
            fv_type = MaterializedFeatureViewType.TEMPORAL

        view_schema = schema.Schema(supplement.view_schema)

        if proto.materialized_feature_view_args.HasField("timestamp_field"):
            timestamp_field = proto.materialized_feature_view_args.timestamp_field
        else:
            timestamp_field = _get_timestamp_column(view_schema)

        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_args_proto(proto.feature_view_id, proto.info),
            entity_ids=tuple(entity_ids),
            join_keys=tuple(join_keys),
            online_serving_keys=tuple(online_serving_keys),
            view_schema=schema.Schema(supplement.view_schema),
            materialization_schema=schema.Schema(supplement.materialization_schema),
            offline_store=utils.get_field_or_none(proto.materialized_feature_view_args, "offline_store"),
            is_continuous=(
                proto.materialized_feature_view_args.stream_processing_mode
                == feature_view__args_pb2.StreamProcessingMode.STREAM_PROCESSING_MODE_CONTINUOUS
            ),
            data_source_type=utils.get_field_or_none(proto.materialized_feature_view_args, "data_source_type"),
            incremental_backfills=proto.materialized_feature_view_args.incremental_backfills,
            timestamp_field=timestamp_field,
            type=fv_type,
            feature_store_format_version=feature_store_pb2.FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_TIME_NANOSECONDS,
            materialization_enabled=False,
            online=proto.online_enabled,
            offline=proto.offline_enabled,
            pipeline=utils.get_field_or_none(proto, "pipeline"),
            batch_schedule=utils.get_duration_field_or_none(proto.materialized_feature_view_args, "batch_schedule"),
            slide_interval=utils.get_duration_field_or_none(
                proto.materialized_feature_view_args, "aggregation_interval"
            ),
            ttl=utils.get_duration_field_or_none(proto.materialized_feature_view_args, "serving_ttl"),
            feature_start_time=utils.get_timestamp_field_or_none(
                proto.materialized_feature_view_args, "feature_start_time"
            ),
            materialization_start_time=utils.get_timestamp_field_or_none(
                proto.materialized_feature_view_args, "feature_start_time"
            ),  # TODO(TEC-12599). This is incorrect for aggregations.
            max_source_data_delay=_get_max_schedule_offset(proto.pipeline),
            aggregate_features=tuple(),  # TODO(TEC-12599)
            slide_interval_string=None,  # TODO(TEC-12599)
            materialized_data_path=None,
            time_range_policy=feature_view__data_pb2.MaterializationTimeRangePolicy.MATERIALIZATION_TIME_RANGE_POLICY_FILTER_TO_RANGE,
            snowflake_view_name=None,
            data_proto=None,
            batch_cluster_config=utils.get_field_or_none(proto.materialized_feature_view_args, "batch_compute"),
        )


@utils.frozen_strict
class OnDemandFeatureViewSpec(FeatureViewSpec):
    # TODO(TEC-12321): Audit and fix feature view spec fields that should be required.
    pipeline: Optional[pipeline_pb2.Pipeline]

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: feature_view__data_pb2.FeatureView) -> "OnDemandFeatureViewSpec":
        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_data_proto(
                proto.feature_view_id, proto.fco_metadata
            ),
            entity_ids=tuple(id_helper.IdHelper.to_string(id) for id in proto.entity_ids),
            join_keys=utils.get_tuple_from_repeated_field(proto.join_keys),
            online_serving_keys=utils.get_tuple_from_repeated_field(proto.online_serving_index.join_keys),
            view_schema=_get_view_schema(proto.schemas),
            materialization_schema=_get_materialization_schema(proto.schemas),
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

    @classmethod
    @typechecked
    def from_args_proto(cls, proto: feature_view__args_pb2.FeatureViewArgs) -> "OnDemandFeatureViewSpec":
        return NotImplementedError


@utils.frozen_strict
class FeatureTableSpec(FeatureViewSpec):
    timestamp_field: str
    ttl: pendulum.Duration

    # TODO(TEC-12321): Audit and fix feature view spec fields that should be required. (batch_cluster_config should be.)
    batch_cluster_config: Optional[feature_view__args_pb2.ClusterConfig]

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: feature_view__data_pb2.FeatureView) -> "FeatureTableSpec":
        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_data_proto(
                proto.feature_view_id, proto.fco_metadata
            ),
            entity_ids=tuple(id_helper.IdHelper.to_string(id) for id in proto.entity_ids),
            join_keys=utils.get_tuple_from_repeated_field(proto.join_keys),
            online_serving_keys=utils.get_tuple_from_repeated_field(proto.online_serving_index.join_keys),
            view_schema=_get_view_schema(proto.schemas),
            materialization_schema=_get_materialization_schema(proto.schemas),
            offline_store=utils.get_field_or_none(proto.materialization_params, "offline_store_config"),
            timestamp_field=utils.get_field_or_none(proto, "timestamp_key"),
            feature_store_format_version=proto.feature_store_format_version,
            materialization_enabled=proto.materialization_enabled,
            online=proto.feature_table.online_enabled,
            offline=proto.feature_table.offline_enabled,
            ttl=utils.get_duration_field_or_none(proto.feature_table, "serving_ttl"),
            materialized_data_path=utils.get_field_or_none(
                proto.enrichments.fp_materialization.materialized_data_location, "path"
            ),
            time_range_policy=utils.get_field_or_none(proto.materialization_params, "time_range_policy"),
            data_proto=proto,
            batch_cluster_config=utils.get_field_or_none(proto.materialization_params, "batch_materialization"),
        )

    @classmethod
    @typechecked
    def from_args_proto(cls, proto: feature_view__args_pb2.FeatureViewArgs) -> "FeatureTableSpec":
        return NotImplementedError


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


@typechecked
def create_feature_view_spec_from_args_proto(
    proto: feature_view__args_pb2.FeatureViewArgs,
    supplement: FeatureViewSpecArgsSupplement,
) -> Optional[Union[MaterializedFeatureViewSpec, OnDemandFeatureViewSpec, FeatureTableSpec]]:
    if proto.HasField("materialized_feature_view_args"):
        return MaterializedFeatureViewSpec.from_args_proto(proto, supplement)
    elif proto.HasField("on_demand_args"):
        return OnDemandFeatureViewSpec.from_args_proto(proto)
    elif proto.HasField("feature_table_args"):
        return FeatureTableSpec.from_args_proto(proto)
    else:
        raise ValueError(f"Unexpect feature view type: {proto}")


def _get_timestamp_column(schema: schema.Schema) -> str:
    timestamp_columns = [column[0] for column in schema.column_name_and_data_types() if column[1] == TimestampType()]
    assert (
        len(timestamp_columns) == 1
    ), f"Attempted to infer timestamp. Expected exactly one timestamp column in schema {schema}"
    return timestamp_columns[0]


def _get_max_schedule_offset(pipeline: pipeline_pb2.Pipeline) -> pendulum.Duration:
    ds_nodes = pipeline_common.get_all_data_source_nodes(pipeline.root)
    assert len(ds_nodes) > 0
    return max([time_utils.proto_to_duration(ds_node.data_source_node.schedule_offset) for ds_node in ds_nodes])
