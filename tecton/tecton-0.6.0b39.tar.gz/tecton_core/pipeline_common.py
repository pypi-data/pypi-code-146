from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import attrs
import pandas
import pendulum

from tecton_core import specs
from tecton_core import time_utils
from tecton_core.id_helper import IdHelper
from tecton_core.materialization_context import BoundMaterializationContext
from tecton_proto.args.pipeline_pb2 import ConstantNode
from tecton_proto.args.pipeline_pb2 import DataSourceNode
from tecton_proto.args.pipeline_pb2 import Input as InputProto
from tecton_proto.args.pipeline_pb2 import Pipeline
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


def unique_node_alias(node: PipelineNode) -> str:
    return f"node_{id(node)}"


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


@attrs.frozen
class PipelineSqlBuilder:
    pipeline: Pipeline
    id_to_transformation: Dict[str, specs.TransformationSpec]
    renamed_inputs_map: Dict[str, str]
    materialization_context: BoundMaterializationContext
    """
    Attributes:
        pipeline: The pipeline proto to generate sql for
        transformations: List of TransformationSpecs that may be referenced by the pipeline.
        renamed_inputs_map: Mapping of input_name (field in PipelineNode) to new alias (how to refer to the input as CTE alias).
            For MaterializedFVs which are the only ones currently supporting sql mode, inputs referenced by input_name are always data sources.
        materialization_context: The materialization context to evaluate the pipeline with.
    """

    def get_queries(self) -> List[Tuple[str, str]]:
        """
        Do a DFS through all transformations in the pipeline. The root of the pipeline should be at the end of the list.
        Each element is a tuple of (node_sql, node_alias).

        Then, to execute the pipeline, just do
            WITH (alias1) as (node_sql1),
            WITH (alias2) as (node_sql2),
            ...
        """
        root = self.pipeline.root
        return self._get_queries_helper(root)

    def _get_queries_helper(self, subtree: PipelineNode) -> List[Tuple[str, str]]:
        ret: List[Tuple[str, str]] = []
        for i in subtree.transformation_node.inputs:
            if i.node.HasField("transformation_node"):
                ret.extend(self._get_queries_helper(i.node))
        ret.append(self._get_query(subtree))
        return ret

    def _node_to_value(self, pipeline_node: PipelineNode):
        """
        This returns the value of the node to be used as the input to the transformation_node that is its parent.
        The transformation defined by the user can look like:
        return f"SELECT {context.end_time} timestamp, d.* from {data_source} d join {transformation_output} t on d.x = t.y + {constant}"
        """
        if pipeline_node.HasField("transformation_node"):
            return unique_node_alias(pipeline_node)
        elif pipeline_node.HasField("data_source_node"):
            return self.renamed_inputs_map[pipeline_node.data_source_node.input_name]
        elif pipeline_node.HasField("materialization_context_node"):
            return self.materialization_context
        elif pipeline_node.HasField("constant_node"):
            return constant_node_to_value(pipeline_node.constant_node)
        else:
            raise NotImplementedError

    def _get_query(self, pipeline_node: PipelineNode) -> Tuple[str, str]:
        """
        Construct a query for the given transformation node.
        Returns a tuple of (query_sql, unique_node_alias).
        The caller will be able to construct a CTE mapping the query_sql to the node_alias.
        """
        assert pipeline_node.HasField("transformation_node")
        transformation_node = pipeline_node.transformation_node
        args: List[Any] = []
        kwargs: Dict[str, Any] = {}
        for transformation_input in transformation_node.inputs:
            node_value = self._node_to_value(transformation_input.node)
            if transformation_input.HasField("arg_index"):
                assert len(args) == transformation_input.arg_index
                args.append(node_value)
            elif transformation_input.HasField("arg_name"):
                kwargs[transformation_input.arg_name] = node_value
            else:
                raise KeyError(f"Unknown argument type for Input node: {transformation_input}")
        transformation = self.id_to_transformation[IdHelper.to_string(transformation_node.transformation_id)]
        user_function = transformation.user_function
        sql = user_function(*args, **kwargs)
        return sql, unique_node_alias(pipeline_node)
