from __future__ import annotations

import datetime
from typing import Dict
from typing import List
from typing import Mapping
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

import attrs
import numpy as np
import pandas
from pyspark.sql import dataframe as pyspark_dataframe
from pyspark.sql import streaming
from typeguard import typechecked

from tecton import conf
from tecton._internals import display
from tecton._internals import errors
from tecton._internals import metadata_service
from tecton._internals import sdk_decorators
from tecton._internals import utils as internal_utils
from tecton.declarative import feature_view as declarative_feature_view
from tecton.declarative import filtered_source
from tecton.features_common import feature_configs
from tecton.interactive import athena_api
from tecton.interactive import data_frame as tecton_dataframe
from tecton.interactive import query_helper
from tecton.interactive import run_api
from tecton.interactive import snowflake_api
from tecton.interactive import spark_api
from tecton.unified import common as unified_common
from tecton.unified import data_source as unified_data_source
from tecton.unified import entity as unified_entity
from tecton.unified import transformation as unified_transformation
from tecton.unified import utils
from tecton_core import errors as core_errors
from tecton_core import fco_container
from tecton_core import feature_definition_wrapper
from tecton_core import feature_set_config
from tecton_core import specs
from tecton_proto.args import fco_args_pb2
from tecton_proto.args import feature_view_pb2 as feature_view__args_pb2
from tecton_proto.common import data_source_type_pb2
from tecton_proto.common import fco_locator_pb2
from tecton_proto.metadataservice import metadata_service_pb2
from tecton_spark import request_context


@attrs.define
class FeatureView(unified_common.BaseTectonObject):
    """Base class for Feature View classes (including Feature Tables).

    Attributes:
        _feature_definition: A FeatureDefinitionWrapper instance, which contains the Feature View spec for this Feature
            View and dependent FCO specs (e.g. Data Source specs). Set only after the object has been validated. Remote
            objects, i.e. applied objects fetched from the backend, are assumed valid.
        _args: A Tecton "args" proto. Only set if this object was defined locally, i.e. this object was not applied
            and fetched from the Tecton backend.
        sources: The Data Sources for this Feature View.
        entities: The Entities for this Feature View.
        tranformations: The Transformations for this Feature View.
    """

    _feature_definition: Optional[feature_definition_wrapper.FeatureDefinitionWrapper] = attrs.field(repr=False)
    _args: Optional[feature_view__args_pb2.FeatureViewArgs] = attrs.field(repr=False, on_setattr=attrs.setters.frozen)

    sources: Tuple[unified_data_source.DataSource, ...] = attrs.field(
        repr=utils.short_tecton_objects_repr, on_setattr=attrs.setters.frozen
    )
    entities: Tuple[unified_entity.Entity, ...] = attrs.field(
        repr=utils.short_tecton_objects_repr, on_setattr=attrs.setters.frozen
    )
    transformations: Tuple[unified_transformation.Transformation, ...] = attrs.field(
        repr=utils.short_tecton_objects_repr, on_setattr=attrs.setters.frozen
    )

    @property
    def _spec(self) -> Optional[specs.FeatureViewSpec]:
        return self._feature_definition.fv_spec if self._feature_definition is not None else None

    def _build_args(self) -> fco_args_pb2.FcoArgs:
        if self._args is None:
            raise errors.BUILD_ARGS_INTERNAL_ERROR

        return fco_args_pb2.FcoArgs(feature_view=self._args)

    @classmethod
    @typechecked
    def _from_spec(cls, spec: specs.FeatureViewSpec, fco_container: fco_container.FcoContainer) -> "FeatureView":
        """Create a FeatureView from directly from a spec. Specs are assumed valid and will not be re-validated."""
        feature_definition = feature_definition_wrapper.FeatureDefinitionWrapper(spec, fco_container)
        info = unified_common.TectonObjectInfo.from_spec(spec)

        sources = []
        for data_source_spec in feature_definition.data_sources:
            if data_source_spec.stream_source is not None:
                sources.append(unified_data_source.StreamSource._from_spec(data_source_spec))
            else:
                sources.append(unified_data_source.BatchSource._from_spec(data_source_spec))

        entities = []
        for entity_spec in feature_definition.entities:
            entities.append(unified_entity.Entity._from_spec(entity_spec))

        transformations = []
        for transformation_spec in feature_definition.transformations:
            transformations.append(unified_transformation.Transformation._from_spec(transformation_spec))

        return cls(
            info=info,
            feature_definition=feature_definition,
            args=None,
            source_info=None,
            sources=tuple(sources),
            entities=tuple(entities),
            transformations=tuple(transformations),
        )

    @property
    def _is_valid(self) -> bool:
        return self._spec is not None

    @sdk_decorators.sdk_public_method
    def validate(self) -> None:
        if self._is_valid:
            # Already valid.
            print("This object has already been validated.")
            return

        print(f"Validating dependencies for feature view {self.info.name}.")
        for dependent_object in self.sources + self.entities + self.transformations:
            dependent_object.validate()

        transformation_specs = [transformation._spec for transformation in self.transformations]
        data_source_specs = [source._spec for source in self.sources]
        entity_specs = [entity._spec for entity in self.entities]

        # TODO(TEC-12599): Implement materialized schema derivation. Needed for aggregate features.
        view_schema = spark_api.derive_view_schema_for_feature_view(self._args, transformation_specs, data_source_specs)
        supplement = specs.FeatureViewSpecArgsSupplement(
            view_schema=spark_api.derive_view_schema_for_feature_view(
                self._args, transformation_specs, data_source_specs
            ),
            materialization_schema=spark_api.derive_view_schema_for_feature_view(
                self._args, transformation_specs, data_source_specs
            ),
        )

        # TODO(jake): Implement backend validation for the feature view.
        fv_spec = specs.create_feature_view_spec_from_args_proto(self._args, supplement)

        fco_container_specs = transformation_specs + data_source_specs + entity_specs + [fv_spec]
        fco_container_ = fco_container.FcoContainer.from_specs(specs=fco_container_specs, root_ids=[fv_spec.id])
        self._feature_definition = feature_definition_wrapper.FeatureDefinitionWrapper(fv_spec, fco_container_)

    @property
    @sdk_decorators.sdk_public_method
    @utils.requires_validation
    def join_keys(self) -> List[str]:
        """The join key column names."""
        return self._feature_definition.join_keys

    @property
    @sdk_decorators.sdk_public_method
    @utils.requires_validation
    def features(self) -> List[str]:
        """The features produced by this FeatureView."""
        return self._feature_definition.features

    @sdk_decorators.sdk_public_method
    @utils.requires_remote_object
    def summary(self) -> display.Displayable:
        """Displays a human readable summary of this data source."""
        request = metadata_service_pb2.GetFeatureViewSummaryRequest(
            fco_locator=fco_locator_pb2.FcoLocator(id=self._spec.id_proto, workspace=self.info.workspace)
        )
        response = metadata_service.instance().GetFeatureViewSummary(request)
        return display.Displayable.from_fco_summary(response.fco_summary)

    def _construct_feature_set_config(self) -> feature_set_config.FeatureSetConfig:
        feature_set_config = feature_set_config.FeatureSetConfig()
        feature_set_config._add(self._feature_definition)
        if self._feature_definition.is_on_demand:
            raise NotImplementedError("ODFVs require adding in depedendent feature view definitions.")
        return feature_set_config

    # TODO(samantha): add delete keys and materialization methods from interactive class


class MaterializedFeatureView(FeatureView):
    """Class for BatchFeatureView and StreamFeatureView to inherit common methods from."""

    @sdk_decorators.sdk_public_method
    @utils.requires_validation
    def get_historical_features(
        self,
        spine: Optional[
            Union[pyspark_dataframe.DataFrame, pandas.DataFrame, tecton_dataframe.TectonDataFrame, str]
        ] = None,
        timestamp_key: Optional[str] = None,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        entities: Optional[
            Union[pyspark_dataframe.DataFrame, pandas.DataFrame, tecton_dataframe.TectonDataFrame]
        ] = None,
        from_source: bool = False,
        save: bool = False,
        save_as: Optional[str] = None,
    ) -> tecton_dataframe.TectonDataFrame:
        """TODO(jake): Port over docs. Deferring to avoid skew while in development."""

        # TODO(jake): Port over get_historical_features() error checking. Deferring because we'll be reworking
        # from_source defaults. See TEC-10489.

        is_dev_workspace = not internal_utils.is_live_workspace(self.info.workspace)
        is_local_mode = self._feature_definition.fv_spec.is_local_object

        if self._feature_definition.is_incremental_backfill:
            if is_local_mode:
                raise errors.FV_WITH_INC_BACKFILLS_GET_MATERIALIZED_FEATURES_IN_LOCAL_MODE(
                    self.name,
                )
            if is_dev_workspace:
                raise errors.FV_WITH_INC_BACKFILLS_GET_MATERIALIZED_FEATURES_FROM_DEVELOPMENT_WORKSPACE(
                    self.name, self.info.workspace
                )
            if from_source:
                raise core_errors.FV_BFC_SINGLE_FROM_SOURCE

        if spine is None and timestamp_key is not None:
            raise errors.GET_HISTORICAL_FEATURES_WRONG_PARAMS(["timestamp_key"], "the spine parameter is not provided")

        if spine is not None and (start_time is not None or end_time is not None or entities is not None):
            raise errors.GET_HISTORICAL_FEATURES_WRONG_PARAMS(
                ["start_time", "end_time", "entities"], "the spine parameter is provided"
            )

        if conf.get_bool("ALPHA_SNOWFLAKE_COMPUTE_ENABLED"):
            return snowflake_api.get_historical_features(
                spine=spine,
                timestamp_key=timestamp_key,
                start_time=start_time,
                end_time=end_time,
                entities=entities,
                from_source=from_source,
                save=save,
                save_as=save_as,
                feature_set_config=self._construct_feature_set_config(),
                append_prefix=False,
            )

        if conf.get_bool("ALPHA_ATHENA_COMPUTE_ENABLED"):
            if self.info.workspace is None or not internal_utils.is_live_workspace(self.info.workspace):
                raise errors.ATHENA_COMPUTE_ONLY_SUPPORTED_IN_LIVE_WORKSPACE

            return athena_api.get_historical_features(
                spine=spine,
                timestamp_key=timestamp_key,
                start_time=start_time,
                end_time=end_time,
                entities=entities,
                from_source=from_source,
                save=save,
                save_as=save_as,
                feature_set_config=self._construct_feature_set_config(),
            )

        return spark_api.get_historical_features_for_feature_definition(
            feature_definition=self._feature_definition,
            spine=spine,
            timestamp_key=timestamp_key,
            start_time=start_time,
            end_time=end_time,
            entities=entities,
            from_source=from_source,
            save=save,
            save_as=save_as,
        )

    @sdk_decorators.sdk_public_method
    @utils.requires_validation
    def run(
        self,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        aggregation_level: Optional[str] = None,
        **mock_sources: Union[pandas.DataFrame, pyspark_dataframe.DataFrame],
    ) -> tecton_dataframe.TectonDataFrame:
        """TODO(samantha): Port over docs."""
        if self._feature_definition.is_temporal and aggregation_level is not None:
            raise errors.FV_UNSUPPORTED_AGGREGATION

        if conf.get_bool("ALPHA_SNOWFLAKE_COMPUTE_ENABLED"):
            return snowflake_api.run_batch(
                fd=self._feature_definition,
                feature_start_time=start_time,
                feature_end_time=end_time,
                mock_inputs=mock_sources,
                aggregate_tiles=None,
                aggregation_level=aggregation_level,
            )

        return run_api.run_batch(
            self._feature_definition,
            start_time,
            end_time,
            mock_sources,
            feature_definition_wrapper.FrameworkVersion.FWV5,
            aggregate_tiles=None,
            aggregation_level=aggregation_level,
        )

    @sdk_decorators.sdk_public_method
    @utils.requires_remote_object
    def get_online_features(
        self,
        join_keys: Mapping[str, Union[int, np.int_, str, bytes]],
        include_join_keys_in_response: bool = False,
    ) -> tecton_dataframe.FeatureVector:
        """TODO(samantha): Port over docs."""
        if not self._feature_definition.writes_to_online_store:
            raise errors.UNSUPPORTED_OPERATION("get_online_features", "online=True is not set for this FeatureView.")
        internal_utils.validate_join_key_types(join_keys)

        return query_helper._QueryHelper(self.info.workspace, feature_view_name=self.info.name).get_feature_vector(
            join_keys or {},
            include_join_keys_in_response,
            {},
            request_context.RequestContext({}),
        )


class BatchFeatureView(MaterializedFeatureView):
    """Tecton class for BatchFeatureViews.

    TODO(samantha): add more info for public docs.
    """


class StreamFeatureView(MaterializedFeatureView):
    """Tecton class for StreamFeatureViews.

    TODO(samantha): add more info for public docs.
    """

    @sdk_decorators.sdk_public_method
    @utils.requires_validation
    def run_stream(self, output_temp_table: str) -> streaming.StreamingQuery:
        """TODO(samantha): Port over docs."""
        return run_api.run_stream(self._feature_definition, output_temp_table)


@typechecked
def batch_feature_view(
    *,
    mode: str,
    sources: Sequence[Union[unified_data_source.BatchSource, filtered_source.FilteredSource]],
    entities: Sequence[unified_entity.Entity],
    aggregation_interval: Optional[datetime.timedelta] = None,
    aggregations: Optional[Sequence[declarative_feature_view.Aggregation]] = None,
    online: Optional[bool] = False,
    offline: Optional[bool] = False,
    ttl: Optional[datetime.timedelta] = None,
    feature_start_time: Optional[datetime.datetime] = None,
    batch_trigger: declarative_feature_view.BatchTriggerType = declarative_feature_view.BatchTriggerType.SCHEDULED,
    batch_schedule: Optional[datetime.timedelta] = None,
    online_serving_index: Optional[Sequence[str]] = None,
    batch_compute: Optional[Union[feature_configs.DatabricksClusterConfig, feature_configs.EMRClusterConfig]] = None,
    offline_store: Optional[
        Union[feature_configs.ParquetConfig, feature_configs.DeltaConfig]
    ] = feature_configs.ParquetConfig(),
    online_store: Optional[Union[feature_configs.DynamoConfig, feature_configs.RedisConfig]] = None,
    monitor_freshness: bool = False,
    expected_feature_freshness: Optional[datetime.timedelta] = None,
    alert_email: Optional[str] = None,
    description: Optional[str] = None,
    owner: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    timestamp_field: Optional[str] = None,
    name: Optional[str] = None,
    max_batch_aggregation_interval: Optional[datetime.timedelta] = None,
    incremental_backfills: bool = False,
):
    """TODO(jake): Port over docs. Deferring to avoid skew while in development."""

    def decorator(user_function):
        from tecton.cli import common as cli_common

        source_info = cli_common.get_fco_source_info()

        if mode == declarative_feature_view.PIPELINE_MODE:
            # TODO(TEC-12574): Support pipeline mode.
            assert False, "Pipeline mode is not currently supported."
            pipeline_function = user_function
            inferred_transform = None
        else:
            # Separate out the Transformation and manually construct a simple pipeline function.
            # We infer owner/family/tags but not a description.
            inferred_transform = unified_transformation.transformation(mode, name, description, owner, tags=tags)(
                user_function
            )

            def pipeline_function(**kwargs):
                return inferred_transform(**kwargs)

        stream_processing_mode = declarative_feature_view.StreamProcessingMode.TIME_INTERVAL if aggregations else None

        args = declarative_feature_view.build_materialized_feature_view_args(
            feature_view_type=feature_view__args_pb2.FeatureViewType.FEATURE_VIEW_TYPE_FWV5_FEATURE_VIEW,
            name=name or user_function.__name__,
            pipeline_function=pipeline_function,
            sources=sources,
            entities=entities,
            online=online,
            offline=offline,
            offline_store=offline_store,
            online_store=online_store,
            aggregation_interval=aggregation_interval,
            stream_processing_mode=stream_processing_mode,
            aggregations=aggregations,
            ttl=ttl,
            feature_start_time=feature_start_time,
            batch_trigger=batch_trigger,
            batch_schedule=batch_schedule,
            online_serving_index=online_serving_index,
            batch_compute=batch_compute,
            stream_compute=None,
            monitor_freshness=monitor_freshness,
            expected_feature_freshness=expected_feature_freshness,
            alert_email=alert_email,
            description=description,
            owner=owner,
            tags=tags,
            timestamp_field=timestamp_field,
            data_source_type=data_source_type_pb2.DataSourceType.BATCH,
            user_function=user_function,
            max_batch_aggregation_interval=max_batch_aggregation_interval,
            output_stream=None,
            incremental_backfills=incremental_backfills,
        )

        info = unified_common.TectonObjectInfo.from_args_proto(args.info, args.feature_view_id)

        data_sources = tuple(
            source.source if isinstance(source, filtered_source.FilteredSource) else source for source in sources
        )

        # TODO(TEC-12574): Support pipeline mode. Will need to get references to all indirectly depended on unified
        # transformation objects.
        return BatchFeatureView(
            info=info,
            feature_definition=None,
            args=args,
            source_info=source_info,
            sources=data_sources,
            entities=tuple(entities),
            transformations=(inferred_transform,),
        )

    return decorator
