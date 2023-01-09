from datetime import datetime
from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple

import pendulum

from tecton_core import errors
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.feature_definition_wrapper import pipeline_to_ds_inputs
from tecton_core.feature_set_config import FeatureDefinitionAndJoinConfig
from tecton_core.feature_set_config import FeatureSetConfig
from tecton_core.id_helper import IdHelper
from tecton_core.pipeline_common import find_dependent_feature_set_items
from tecton_core.pipeline_common import get_time_window_from_data_source_node
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.node_utils import AsofJoinInputContainer
from tecton_core.query.nodes import AddDurationNode
from tecton_core.query.nodes import AsofJoinNode
from tecton_core.query.nodes import DataNode
from tecton_core.query.nodes import DataSourceScanNode
from tecton_core.query.nodes import EFFECTIVE_TIMESTAMP
from tecton_core.query.nodes import EffectiveTimestampNode
from tecton_core.query.nodes import EXPIRATION_TIMESTAMP
from tecton_core.query.nodes import FeatureTimeFilterNode
from tecton_core.query.nodes import FeatureViewPipelineNode
from tecton_core.query.nodes import FullAggNode
from tecton_core.query.nodes import JoinNode
from tecton_core.query.nodes import MetricsCollectorNode
from tecton_core.query.nodes import OdfvPipelineNode
from tecton_core.query.nodes import OfflineStoreScanNode
from tecton_core.query.nodes import PartialAggNode
from tecton_core.query.nodes import RenameColsNode
from tecton_core.query.nodes import RespectFSTNode
from tecton_core.query.nodes import RespectTTLNode
from tecton_core.query.nodes import SetAnchorTimeNode
from tecton_core.query.nodes import StreamWatermarkNode
from tecton_proto.args.pipeline_pb2 import DataSourceNode as ProtoDataSourceNode
from tecton_proto.data.virtual_data_source_pb2 import VirtualDataSource

ANCHOR_TIME = "_anchor_time"
WINDOW_END_COLUMN_NAME = "tile_end_time"


def build_datasource_scan_node(
    ds: VirtualDataSource, for_stream: bool, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None
) -> NodeRef:
    return DataSourceScanNode(
        ds,
        ds_node=None,
        is_stream=for_stream,
        start_time=start_time,
        end_time=end_time,
    ).as_ref()


def _get_ds_time_limits(
    feature_data_time_limits: Optional[pendulum.Period],
    schedule_interval: Optional[pendulum.Duration],
    data_source_node: ProtoDataSourceNode,
) -> Tuple[Optional[datetime], Optional[datetime]]:
    ds_time_limits = get_time_window_from_data_source_node(
        feature_data_time_limits, schedule_interval, data_source_node
    )
    if ds_time_limits:
        return ds_time_limits.start, ds_time_limits.end
    return None, None


def build_datasource_input_querynodes(
    fdw: FeatureDefinitionWrapper, for_stream: bool, feature_data_time_limits: Optional[pendulum.Period] = None
) -> Dict[str, NodeRef]:
    """
    Starting in FWV5, data sources of FVs with incremental backfills may contain transformations that are only
    correct if the data has been filtered to a specific range.
    """
    schedule_interval = fdw.get_tile_interval if fdw.is_temporal else None
    ds_inputs = pipeline_to_ds_inputs(fdw.pipeline)

    input_querynodes = {}
    for input_name, node in ds_inputs.items():
        start_time, end_time = _get_ds_time_limits(feature_data_time_limits, schedule_interval, node)
        input_querynodes[input_name] = DataSourceScanNode(
            ds=fdw.fco_container.get_by_id(IdHelper.to_string(node.virtual_data_source_id)),
            ds_node=node,
            is_stream=for_stream,
            start_time=start_time,
            end_time=end_time,
        ).as_ref()
    return input_querynodes


def get_stream_watermark(fdw: FeatureDefinitionWrapper) -> Optional[str]:
    ds_inputs = pipeline_to_ds_inputs(fdw.pipeline)
    for input_name, node in ds_inputs.items():
        virtual_ds = fdw.fco_container.get_by_id(IdHelper.to_string(node.virtual_data_source_id))
        if virtual_ds.stream_data_source is not None:
            stream_data_source = virtual_ds.stream_data_source
            watermark_delay_threshold_seconds = stream_data_source.stream_config.watermark_delay_threshold.seconds
            # NOTE: we do not want to set an explicit '0 seconds' watermark as
            # that can lead to data loss (data source functions supports
            # user-specified watermark configuration in function).
            if watermark_delay_threshold_seconds:
                return f"{watermark_delay_threshold_seconds} seconds"
    return None


# build QueryTree that executes all transformations
def build_pipeline_querytree(
    fdw: FeatureDefinitionWrapper, for_stream: bool, feature_data_time_limits: Optional[pendulum.Period] = None
) -> NodeRef:
    inputs_map = build_datasource_input_querynodes(fdw, for_stream, feature_data_time_limits)
    return FeatureViewPipelineNode(
        inputs_map=inputs_map,
        feature_definition_wrapper=fdw,
        feature_time_limits=feature_data_time_limits,
    ).as_ref()


# builds a QueryTree for just whatever we would materialize
# ie partial aggregates for WAFVs.
def build_run_querytree(
    fdw: FeatureDefinitionWrapper,
    for_stream: bool,
    feature_data_time_limits: Optional[pendulum.Period] = None,
    include_window_end_time: bool = False,
    aggregation_anchor_time: Optional[datetime] = None,
    enable_feature_metrics: bool = False,
) -> NodeRef:
    assert not for_stream or feature_data_time_limits is None, "Cannot run with time limits on a stream source"
    base = build_pipeline_querytree(fdw, for_stream, feature_data_time_limits)
    if for_stream:
        watermark = get_stream_watermark(fdw)
        if watermark:
            base = StreamWatermarkNode(base, fdw.time_key, watermark).as_ref()

    tree = FeatureTimeFilterNode(
        base,
        feature_data_time_limits=feature_data_time_limits,
        policy=fdw.time_range_policy,
        timestamp_field=fdw.timestamp_key,
    ).as_ref()
    if enable_feature_metrics:
        tree = MetricsCollectorNode(tree).as_ref()
    if fdw.is_temporal:
        assert not include_window_end_time, "Not supported window end time for temporal"
        tree = SetAnchorTimeNode(
            tree,
            offline=True,
            feature_store_format_version=fdw.get_feature_store_format_version,
            batch_schedule_in_feature_store_specific_version_units=fdw.get_batch_schedule_for_version,
            tile_version_in_feature_store_specific_version_units=fdw.get_tile_interval_for_version,
            timestamp_field=fdw.timestamp_key,
            is_stream=for_stream,
            for_retrieval=False,
            # used only for retrieval
            data_delay_seconds=None,
        ).as_ref()
    elif fdw.is_temporal_aggregate:
        window_end_column_name = WINDOW_END_COLUMN_NAME if include_window_end_time else None
        tree = PartialAggNode(tree, fdw, ANCHOR_TIME, window_end_column_name, aggregation_anchor_time).as_ref()
    else:
        raise Exception("unexpected FV type")
    return tree


def build_get_features(
    fdw: FeatureDefinitionWrapper,
    from_source: bool,
    feature_data_time_limits: Optional[pendulum.Period] = None,
    aggregation_anchor_time: Optional[datetime] = None,
):
    if not from_source:
        assert not aggregation_anchor_time, "aggregation anchor time is not allowed when fetching features from source"
        if not fdw.writes_to_offline_store:
            raise errors.FV_NEEDS_TO_BE_MATERIALIZED(fdw.name)
        return OfflineStoreScanNode(feature_definition_wrapper=fdw, time_filter=feature_data_time_limits).as_ref()
    else:
        if fdw.is_incremental_backfill:
            raise errors.FV_BFC_SINGLE_FROM_SOURCE
        return build_run_querytree(
            fdw,
            for_stream=False,
            feature_data_time_limits=feature_data_time_limits,
            aggregation_anchor_time=aggregation_anchor_time,
        )


def build_get_full_agg_features(
    fdw: FeatureDefinitionWrapper,
    spine: NodeRef,
    from_source: bool,
    feature_data_time_limits: Optional[pendulum.Period] = None,
    respect_feature_start_time: bool = True,
    aggregation_anchor_time: Optional[datetime] = None,
):
    base = build_get_features(
        fdw,
        from_source,
        feature_data_time_limits=feature_data_time_limits,
        aggregation_anchor_time=aggregation_anchor_time,
    )
    return FullAggNode(base, fdw, spine, respect_feature_start_time=respect_feature_start_time).as_ref()


def build_spine_join_querytree(
    dac: FeatureDefinitionAndJoinConfig, spine: Any, spine_time_field: str, from_source: bool
) -> NodeRef:
    fdw = dac.feature_definition
    spine_node = DataNode(spine).as_ref()
    if spine_time_field != fdw.timestamp_key:
        spine_node = RenameColsNode(spine_node, {spine_time_field: fdw.timestamp_key}).as_ref()
    if any([jk[0] != jk[1] for jk in dac.join_keys]):
        spine_node = RenameColsNode(spine_node, {jk[0]: jk[1] for jk in dac.join_keys if jk[0] != jk[1]}).as_ref()

    if fdw.is_temporal or fdw.is_feature_table:
        ret = _build_spine_query_tree_temporal_or_feature_table(
            spine_node=spine_node,
            dac=dac,
            data_delay_seconds=fdw.online_store_data_delay_seconds,
            from_source=from_source,
        )
    elif fdw.is_temporal_aggregate:
        augmented_spine = SetAnchorTimeNode(
            spine_node,
            offline=True,
            feature_store_format_version=fdw.get_feature_store_format_version,
            batch_schedule_in_feature_store_specific_version_units=fdw.get_batch_schedule_for_version,
            tile_version_in_feature_store_specific_version_units=fdw.get_tile_interval_for_version,
            timestamp_field=fdw.timestamp_key,
            is_stream=fdw.is_stream,
            for_retrieval=True,
            data_delay_seconds=fdw.online_store_data_delay_seconds,
        ).as_ref()
        base = build_get_full_agg_features(
            fdw,
            spine=augmented_spine,
            from_source=from_source,
            respect_feature_start_time=True,
        )
        rename_map = {}
        for f in fdw.features:
            if f not in dac.features:
                rename_map[f] = None
            else:
                rename_map[f] = f"{dac.namespace}{fdw.namespace_separator}{f}"
        right = RenameColsNode(base, rename_map).as_ref()
        join_keys = fdw.join_keys + [ANCHOR_TIME]
        # TODO: can consider having "inner" be an enum. right now join type as string can be passed directly to spark/snowflake
        join = JoinNode(augmented_spine, right, how="inner", join_cols=join_keys).as_ref()
        # Drop anchor time col
        ret = RenameColsNode(join, {ANCHOR_TIME: None}).as_ref()
    elif fdw.is_on_demand:
        inputs = find_dependent_feature_set_items(
            fdw.fco_container,
            fdw.pipeline.root,
            visited_inputs={},
            fv_id=fdw.id,
            workspace_name=fdw.workspace,
        )
        dac = FeatureDefinitionAndJoinConfig.from_feature_definition(fdw)
        fsc = FeatureSetConfig(inputs + [dac])
        ret = build_feature_set_config_querytree(fsc, spine, spine_time_field, from_source)
    else:
        raise NotImplementedError
    if spine_time_field != fdw.timestamp_key:
        ret = RenameColsNode(ret, {fdw.timestamp_key: spine_time_field}).as_ref()
    if any([jk[0] != jk[1] for jk in dac.join_keys]):
        ret = RenameColsNode(ret, {jk[1]: jk[0] for jk in dac.join_keys if jk[0] != jk[1]}).as_ref()
    return ret


# Construct each materialized fvtree by joining against distinct set of join keys.
# Then, join the full spine against each of those.
# Finally, compute odfvs via udf on top of the result (not using joins)
def build_feature_set_config_querytree(
    fsc: FeatureSetConfig, spine: Any, spine_time_field: str, from_source: bool
) -> NodeRef:
    spine_node = DataNode(spine).as_ref()
    spine_join_keys = fsc.join_keys
    newtree = spine_node
    odfv_dacs = [dac for dac in fsc._definitions_and_configs if dac.feature_definition.is_on_demand]
    other_dacs = [dac for dac in fsc._definitions_and_configs if not dac.feature_definition.is_on_demand]
    internal_cols = set()
    # do all non on-demand first
    for dac in other_dacs:
        fdw = dac.feature_definition
        subspine_join_keys = [jk[0] for jk in dac.join_keys]
        if dac.namespace.startswith("_udf_internal"):
            for feature in fdw.features:
                internal_cols.add(dac.namespace + fdw.namespace_separator + feature)
        for feature in dac.features:
            if "_udf_internal" in feature:
                internal_cols.add(feature)
        subspine = spine.select([jk[0] for jk in dac.join_keys] + [spine_time_field]).distinct()
        fvtree = build_spine_join_querytree(dac, subspine, spine_time_field, from_source)
        if len(dac.features) < len(fdw.features):
            fvtree = RenameColsNode(
                fvtree, {f"{fdw.name}{fdw.namespace_separator}{f}": None for f in fdw.features if f not in dac.features}
            ).as_ref()
        newtree = JoinNode(newtree, fvtree, how="inner", join_cols=subspine_join_keys + [spine_time_field]).as_ref()
    # do all on-demand next
    for dac in odfv_dacs:
        fdw = dac.feature_definition
        newtree = OdfvPipelineNode(newtree, fdw, dac.namespace).as_ref()
        if len(dac.features) < len(fdw.features):
            drop_map = {
                f"{dac.namespace}{fdw.namespace_separator}{f}": None for f in fdw.features if f not in dac.features
            }
            newtree = RenameColsNode(newtree, drop_map).as_ref()
    # drop all internal cols
    if len(internal_cols) > 0:
        newtree = RenameColsNode(newtree, {col: None for col in internal_cols}).as_ref()

    return newtree


def _build_spine_query_tree_temporal_or_feature_table(
    spine_node: NodeRef, dac: FeatureDefinitionAndJoinConfig, data_delay_seconds: int, from_source: bool
):
    TIMESTAMP_PLUS_TTL = "_timestamp_plus_ttl"
    fdw = dac.feature_definition
    base = build_get_features(fdw, from_source=from_source)
    base = EffectiveTimestampNode(
        base,
        timestamp_field=fdw.timestamp_key,
        effective_timestamp_name=EFFECTIVE_TIMESTAMP,
        batch_schedule_seconds=fdw.fv.materialization_params.schedule_interval.ToTimedelta().total_seconds(),
        data_delay_seconds=data_delay_seconds,
        for_stream=fdw.is_stream,
        is_temporal_aggregate=False,
    ).as_ref()
    base = AddDurationNode(
        base, timestamp_field=fdw.timestamp_key, duration=fdw.serving_ttl, new_column_name=TIMESTAMP_PLUS_TTL
    ).as_ref()
    # Calculate effective expiration time = window(feature_time + ttl, batch_schedule).end + data_delay
    base = EffectiveTimestampNode(
        base,
        timestamp_field=TIMESTAMP_PLUS_TTL,
        effective_timestamp_name=EXPIRATION_TIMESTAMP,
        batch_schedule_seconds=fdw.batch_materialization_schedule.total_seconds(),
        data_delay_seconds=data_delay_seconds,
        for_stream=fdw.is_stream,
        is_temporal_aggregate=False,
    ).as_ref()
    rightside_join_prefix = "_tecton_right"
    join_prefixed_feature_names = [f"{rightside_join_prefix}_{f}" for f in fdw.features]
    # we can't just ask for the correct right_prefix to begin with because the asofJoin always sticks an extra underscore in between
    rename_map = {
        f"{rightside_join_prefix}_{f}": f"{dac.namespace}{fdw.namespace_separator}{f}"
        for f in fdw.features
        if f in dac.features
    }
    for f in fdw.features:
        if f not in dac.features:
            rename_map[f"{rightside_join_prefix}_{f}"] = None
        else:
            rename_map[f"{rightside_join_prefix}_{f}"] = f"{dac.namespace}{fdw.namespace_separator}{f}"

    expiration_timestamp_col = f"{rightside_join_prefix}_{EXPIRATION_TIMESTAMP}"

    rename_map[f"{rightside_join_prefix}_{fdw.timestamp_key}"] = None
    rename_map[f"{rightside_join_prefix}_{ANCHOR_TIME}"] = None
    rename_map[f"{rightside_join_prefix}_{EFFECTIVE_TIMESTAMP}"] = None
    rename_map[f"{rightside_join_prefix}_{TIMESTAMP_PLUS_TTL}"] = None
    rename_map[expiration_timestamp_col] = None

    if fdw.feature_start_timestamp is not None:
        base = RespectFSTNode(base, fdw.timestamp_key, fdw.feature_start_timestamp, fdw.features).as_ref()
    join = AsofJoinNode(
        left_container=AsofJoinInputContainer(spine_node, fdw.timestamp_key),
        right_container=AsofJoinInputContainer(
            base,
            timestamp_field=fdw.timestamp_key,
            effective_timestamp_field=EFFECTIVE_TIMESTAMP,
            prefix=rightside_join_prefix,
        ),
        join_cols=fdw.join_keys,
    ).as_ref()

    ttl_node = RespectTTLNode(join, fdw.timestamp_key, expiration_timestamp_col, join_prefixed_feature_names).as_ref()
    # remove anchor cols/dupe timestamp cols
    return RenameColsNode(ttl_node, rename_map).as_ref()
