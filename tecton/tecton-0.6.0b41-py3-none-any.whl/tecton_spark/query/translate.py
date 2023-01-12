import sys
import typing

import attrs

from tecton_core.query.node_interface import NodeRef
from tecton_core.query.nodes import AddAnchorTimeNode
from tecton_core.query.nodes import AddDurationNode
from tecton_core.query.nodes import AddEffectiveTimestampNode
from tecton_core.query.nodes import AddRetrievalAnchorTimeNode
from tecton_core.query.nodes import AsofJoinFullAggNode
from tecton_core.query.nodes import AsofJoinInputContainer
from tecton_core.query.nodes import AsofJoinNode
from tecton_core.query.nodes import AsofWildcardExplodeNode
from tecton_core.query.nodes import ConvertEpochToTimestampNode
from tecton_core.query.nodes import CustomFilterNode
from tecton_core.query.nodes import DataSourceScanNode
from tecton_core.query.nodes import EntityFilterNode
from tecton_core.query.nodes import FeatureTimeFilterNode
from tecton_core.query.nodes import FeatureViewPipelineNode
from tecton_core.query.nodes import JoinNode
from tecton_core.query.nodes import MetricsCollectorNode
from tecton_core.query.nodes import MockDataSourceScanNode
from tecton_core.query.nodes import OdfvPipelineNode
from tecton_core.query.nodes import OfflineStoreScanNode
from tecton_core.query.nodes import PartialAggNode
from tecton_core.query.nodes import RawDataSourceScanNode
from tecton_core.query.nodes import RenameColsNode
from tecton_core.query.nodes import RespectFeatureStartTimeNode
from tecton_core.query.nodes import RespectTTLNode
from tecton_core.query.nodes import SelectDistinctNode
from tecton_core.query.nodes import StreamWatermarkNode
from tecton_core.query.nodes import UserSpecifiedDataNode
from tecton_core.query.nodes import WildcardJoinNode
from tecton_spark.query import data_source
from tecton_spark.query import filter
from tecton_spark.query import join
from tecton_spark.query import pipeline
from tecton_spark.query import projection
from tecton_spark.query.node import SparkExecNode

if sys.version_info >= (3, 9):
    from typing import get_args, get_origin
else:
    from typing_extensions import get_args, get_origin


# convert from logical tree to physical tree
def spark_convert(node_ref: NodeRef) -> SparkExecNode:
    logical_tree_node = node_ref.node
    node_mapping = {
        CustomFilterNode: filter.CustomFilterSparkNode,
        DataSourceScanNode: data_source.DataSourceScanSparkNode,
        RawDataSourceScanNode: data_source.RawDataSourceScanSparkNode,
        MockDataSourceScanNode: data_source.MockDataSourceScanSparkNode,
        OfflineStoreScanNode: data_source.OfflineStoreScanSparkNode,
        FeatureViewPipelineNode: pipeline.PipelineEvalSparkNode,
        OdfvPipelineNode: pipeline.OdfvPipelineSparkNode,
        FeatureTimeFilterNode: filter.FeatureTimeFilterSparkNode,
        EntityFilterNode: filter.EntityFilterSparkNode,
        RespectTTLNode: filter.RespectTTLSparkNode,
        RespectFeatureStartTimeNode: filter.RespectFeatureStartTimeSparkNode,
        AddAnchorTimeNode: projection.AddAnchorTimeSparkNode,
        AddRetrievalAnchorTimeNode: projection.AddRetrievalAnchorTimeSparkNode,
        StreamWatermarkNode: filter.StreamWatermarkSparkNode,
        UserSpecifiedDataNode: data_source.UserSpecifiedDataSparkNode,
        PartialAggNode: pipeline.PartialAggSparkNode,
        JoinNode: join.JoinSparkNode,
        WildcardJoinNode: join.WildcardJoinSparkNode,
        AsofJoinNode: join.AsofJoinSparkNode,
        AsofJoinFullAggNode: join.AsofJoinFullAggSparkNode,
        AsofWildcardExplodeNode: join.AsofWildcardExplodeSparkNode,
        RenameColsNode: projection.RenameColsSparkNode,
        SelectDistinctNode: projection.SelectDistinctSparkNode,
        ConvertEpochToTimestampNode: projection.ConvertEpochToTimestampSparkNode,
        AddEffectiveTimestampNode: projection.AddEffectiveTimestampSparkNode,
        MetricsCollectorNode: pipeline.MetricsCollectorSparkNode,
        SelectDistinctNode: projection.SelectDistinctSparkNode,
        AddDurationNode: projection.AddDurationSparkNode,
    }

    if logical_tree_node.__class__ in node_mapping:
        return node_mapping[logical_tree_node.__class__].from_query_node(logical_tree_node)

    raise Exception(f"TODO: mapping for {logical_tree_node.__class__}")


def attrs_spark_converter(attrs_inst: typing.Any, attr: attrs.Attribute, item: typing.Any) -> typing.Any:
    """
    This converts a NodeRef into a SparkNode if it's a NodeRef.
    """
    # Check if type is a typing wrapper.
    if get_origin(attr.type) is not None:
        if get_origin(attr.type) == typing.Union and NodeRef in get_args(attr.type) and isinstance(item, NodeRef):
            return spark_convert(item)
        elif get_origin(attr.type) == dict and NodeRef == get_args(attr.type)[1]:
            return {k: spark_convert(v) for k, v in item.items()}
        return item
    if attr.type == NodeRef:
        return spark_convert(item)
    if attr.type == AsofJoinInputContainer:
        return join.AsofJoinInputSparkContainer(
            **attrs.asdict(item, value_serializer=attrs_spark_converter, recurse=False)
        )
    return item
