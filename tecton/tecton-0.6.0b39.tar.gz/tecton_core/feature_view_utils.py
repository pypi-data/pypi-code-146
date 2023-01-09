from typing import List
from typing import Mapping
from typing import Union

from google.protobuf import duration_pb2
from typeguard import typechecked

from tecton_core.time_utils import to_human_readable_str
from tecton_proto.args import feature_view_pb2
from tecton_proto.common.aggregation_function_pb2 import AggregationFunctionParams
from tecton_proto.common.schema_pb2 import Schema as SchemaProto

CONTINUOUS_MODE_BATCH_INTERVAL = duration_pb2.Duration(seconds=86400)


def get_input_feature_columns(view_schema: SchemaProto, join_keys: List[str], timestamp_key: str) -> List[str]:
    column_names = (c.name for c in view_schema.columns)
    return [c for c in column_names if c not in join_keys and c != timestamp_key]


@typechecked
def construct_aggregation_output_feature_name(
    column: str,
    function: str,
    window: duration_pb2.Duration,
    aggregation_interval: duration_pb2.Duration,
    is_continuous: bool,
):
    window_name = to_human_readable_str(window)
    if is_continuous:
        aggregation_interval_name = "continuous"
    else:
        aggregation_interval_name = to_human_readable_str(aggregation_interval)
    return f"{column}_{function}_{window_name}_{aggregation_interval_name}".replace(" ", "")


def resolve_function_name(
    function_name: str, params: Union[AggregationFunctionParams, Mapping[str, feature_view_pb2.ParamValue]]
) -> str:
    if isinstance(params, AggregationFunctionParams):
        return _resolve_function_name_from_data_proto(function_name, params)
    return _resolve_function_name_from_arg_proto(function_name, params)


def _resolve_function_name_from_arg_proto(function_name: str, params: Mapping[str, feature_view_pb2.ParamValue]):
    if function_name == "lastn":
        return f"last_distinct_{params['n'].int64_value}"
    elif function_name == "last_non_distinct_n":
        return f"last_{params['n'].int64_value}"
    elif function_name == "first_non_distinct_n":
        return f"first_{params['n'].int64_value}"
    elif function_name == "first_distinct_n":
        return f"first_distinct_{params['n'].int64_value}"
    else:
        return function_name


def _resolve_function_name_from_data_proto(function_name: str, params: AggregationFunctionParams):
    if function_name == "lastn":
        return f"last_distinct_{params.last_n.n }"
    elif function_name == "last_non_distinct_n":
        return f"last_{params.last_n.n }"
    elif function_name == "first_non_distinct_n":
        return f"first_{params.first_n.n }"
    elif function_name == "first_distinct_n":
        return f"first_distinct_{params.first_n.n }"
    else:
        return function_name
