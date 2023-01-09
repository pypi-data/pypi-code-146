from tecton_core.query.node_interface import NodeRef
from tecton_core.query.nodes import AddDurationNode
from tecton_core.query.nodes import AsofJoinNode
from tecton_core.query.nodes import ConvertEpochToTimestamp
from tecton_core.query.nodes import CustomFilterNode
from tecton_core.query.nodes import DataNode
from tecton_core.query.nodes import DataSourceScanNode
from tecton_core.query.nodes import EffectiveTimestampNode
from tecton_core.query.nodes import EntityFilterNode
from tecton_core.query.nodes import FeatureTimeFilterNode
from tecton_core.query.nodes import FeatureViewPipelineNode
from tecton_core.query.nodes import FullAggNode
from tecton_core.query.nodes import JoinNode
from tecton_core.query.nodes import MetricsCollectorNode
from tecton_core.query.nodes import MockDataSourceScanNode
from tecton_core.query.nodes import OdfvPipelineNode
from tecton_core.query.nodes import OfflineStoreScanNode
from tecton_core.query.nodes import PartialAggNode
from tecton_core.query.nodes import RawDataSourceScanNode
from tecton_core.query.nodes import RenameColsNode
from tecton_core.query.nodes import RespectFSTNode
from tecton_core.query.nodes import RespectTTLNode
from tecton_core.query.nodes import SetAnchorTimeNode
from tecton_core.query.nodes import StreamWatermarkNode
from tecton_core.query.nodes import TimeFilterNode
from tecton_spark.query import data_source
from tecton_spark.query import filter
from tecton_spark.query import join
from tecton_spark.query import pipeline
from tecton_spark.query import projection
from tecton_spark.query.node import SparkExecNode

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
        TimeFilterNode: filter.TimeFilterSparkNode,
        RespectTTLNode: filter.RespectTTLSparkNode,
        RespectFSTNode: filter.RespectFSTSparkNode,
        SetAnchorTimeNode: projection.SetAnchorTimeSparkNode,
        StreamWatermarkNode: filter.StreamWatermarkSparkNode,
        DataNode: data_source.DataSparkNode,
        PartialAggNode: pipeline.PartialAggSparkNode,
        JoinNode: join.JoinSparkNode,
        AsofJoinNode: join.AsofJoinSparkNode,
        FullAggNode: pipeline.FullAggSparkNode,
        RenameColsNode: projection.RenameColsSparkNode,
        ConvertEpochToTimestamp: projection.ConvertEpochToTimestampSparkNode,
        EffectiveTimestampNode: projection.EffectiveTimestampSparkNode,
        MetricsCollectorNode: pipeline.MetricsCollectorSparkNode,
        AddDurationNode: projection.AddDurationSparkNode,
    }

    if logical_tree_node.__class__ in node_mapping:
        return node_mapping[logical_tree_node.__class__](logical_tree_node)
    else:
        raise Exception(f"TODO: mapping for {logical_tree_node.__class__}")
