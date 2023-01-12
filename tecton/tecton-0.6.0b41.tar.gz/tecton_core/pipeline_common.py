from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pandas
import pendulum

from tecton_core import time_utils
from tecton_proto.args.pipeline_pb2 import ConstantNode
from tecton_proto.args.pipeline_pb2 import DataSourceNode
from tecton_proto.args.pipeline_pb2 import Input as InputProto
from tecton_proto.args.pipeline_pb2 import PipelineNode
from tecton_proto.args.pipeline_pb2 import RequestContext as RequestContextProto

CONSTANT_TYPE = Optional[Union[str, int, float, bool]]
CONSTANT_TYPE_OBJECTS = (str, int, float, bool)


def _make_mode_to_type() -> Dict[str, Any]:
    lookup: Dict[str, Any] = {
        "pandas": pandas.DataFrame,
        "python": Dict,
        "pipeline": PipelineNode,
        "spark_sql": str,
        "snowflake_sql": str,
        "athena": str,
    }
    try:
        import pyspark.sql

        lookup["pyspark"] = pyspark.sql.DataFrame
    except ImportError:
        pass
    try:
        import snowflake.snowpark

        lookup["snowpark"] = snowflake.snowpark.DataFrame
    except ImportError:
        pass
    return lookup


MODE_TO_TYPE_LOOKUP: Dict[str, Any] = _make_mode_to_type()


def constant_node_to_value(constant_node: ConstantNode) -> CONSTANT_TYPE:
    if constant_node.HasField("string_const"):
        return constant_node.string_const
    elif constant_node.HasField("int_const"):
        return int(constant_node.int_const)
    elif constant_node.HasField("float_const"):
        return float(constant_node.float_const)
    elif constant_node.HasField("bool_const"):
        return constant_node.bool_const
    elif constant_node.HasField("null_const"):
        return None
    raise KeyError(f"Unknown ConstantNode type: {constant_node}")


def get_keyword_inputs(transformation_node) -> Dict[str, InputProto]:
    """Returns the keyword inputs of transformation_node in a dict."""
    return {
        node_input.arg_name: node_input for node_input in transformation_node.inputs if node_input.HasField("arg_name")
    }


def positional_inputs(transformation_node) -> List[InputProto]:
    """Returns the positional inputs of transformation_node in order."""
    return [node_input for node_input in transformation_node.inputs if node_input.HasField("arg_index")]


def transformation_type_checker(object_name, result, mode: str, supported_modes) -> None:
    possible_mode = None
    for candidate_mode, candidate_type in MODE_TO_TYPE_LOOKUP.items():
        if isinstance(result, candidate_type):
            possible_mode = candidate_mode
            break
    expected_type = MODE_TO_TYPE_LOOKUP[mode]
    actual_type = type(result)

    if isinstance(result, expected_type):
        return
    elif possible_mode is not None and possible_mode in supported_modes:
        raise TypeError(
            f"Transformation function {object_name} with mode '{mode}' is expected to return result with type {expected_type}, but returns result with type {actual_type} instead. Did you mean to set mode='{possible_mode}'?"
        )
    else:
        raise TypeError(
            f"Transformation function {object_name} with mode {mode} is expected to return result with type {expected_type}, but returns result with type {actual_type} instead."
        )


def get_time_window_from_data_source_node(
    feature_time_limits: Optional[pendulum.Period],
    schedule_interval: Optional[pendulum.Duration],
    data_source_node: DataSourceNode,
) -> Optional[pendulum.Period]:
    if data_source_node.HasField("window") and feature_time_limits:
        new_start = feature_time_limits.start - time_utils.proto_to_duration(data_source_node.window)
        if schedule_interval:
            new_start = new_start + schedule_interval
        raw_data_limits = pendulum.Period(new_start, feature_time_limits.end)
    elif data_source_node.HasField("window_unbounded_preceding") and feature_time_limits:
        raw_data_limits = pendulum.Period(pendulum.datetime(1970, 1, 1), feature_time_limits.end)
    elif data_source_node.HasField("start_time_offset") and feature_time_limits:
        new_start = feature_time_limits.start + time_utils.proto_to_duration(data_source_node.start_time_offset)
        raw_data_limits = pendulum.Period(new_start, feature_time_limits.end)
    elif data_source_node.HasField("window_unbounded"):
        raw_data_limits = None
    else:
        # no data_source_override has been set
        raw_data_limits = feature_time_limits
    return raw_data_limits


def find_request_context(node: PipelineNode) -> Optional[RequestContextProto]:
    """Returns the request context for the pipeline. Assumes there is at most one RequestContext."""
    if node.HasField("request_data_source_node"):
        return node.request_data_source_node.request_context
    elif node.HasField("transformation_node"):
        for child in node.transformation_node.inputs:
            rc = find_request_context(child.node)
            if rc is not None:
                return rc
    return None


def get_all_data_source_nodes(root: PipelineNode) -> List[PipelineNode]:
    """Returns all data source nodes from the provided root."""
    return [node for node in get_all_pipeline_nodes(root) if node.HasField("data_source_node")]


def get_all_pipeline_nodes(node: PipelineNode) -> List[PipelineNode]:
    """Returns all data source nodes from the provided node."""
    if node.HasField("transformation_node"):
        return sum([get_all_pipeline_nodes(input.node) for input in node.transformation_node.inputs], [])
    else:
        return [node]
