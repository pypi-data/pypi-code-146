import secrets
from dataclasses import dataclass
from textwrap import dedent
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import pandas as pd
import pendulum
import sqlparse

from tecton_athena.templates_utils import load_template
from tecton_core import specs
from tecton_core.errors import TectonInternalError
from tecton_core.errors import TectonValidationError
from tecton_core.errors import UDF_ERROR
from tecton_core.id_helper import IdHelper
from tecton_core.materialization_context import BaseMaterializationContext
from tecton_core.pipeline_common import constant_node_to_value
from tecton_core.pipeline_common import CONSTANT_TYPE
from tecton_core.pipeline_common import CONSTANT_TYPE_OBJECTS
from tecton_core.pipeline_common import get_keyword_inputs
from tecton_core.pipeline_common import get_time_window_from_data_source_node
from tecton_core.pipeline_common import positional_inputs
from tecton_core.pipeline_common import transformation_type_checker
from tecton_proto.args.pipeline_pb2 import DataSourceNode
from tecton_proto.args.pipeline_pb2 import Pipeline
from tecton_proto.args.pipeline_pb2 import PipelineNode
from tecton_proto.args.pipeline_pb2 import TransformationNode
from tecton_proto.args.transformation_pb2 import TransformationMode


DATA_SOURCE_TEMPLATE = load_template("data_source.sql")
TIME_LIMIT_TEMPLATE = load_template("time_limit.sql")
PIPELINE_TEMPLATE = load_template("transformation_pipeline.sql")
TEMP_DS_PREFIX = "_TT_DS_"
TEMP_CTE_PREFIX = "_TT_CTE_"


def pipeline_to_sql_string(
    pipeline: Pipeline,
    data_sources: List[specs.DataSourceSpec],
    transformations: List[specs.TransformationSpec],
    materialization_context: BaseMaterializationContext,
    mock_sql_inputs: Optional[Dict[str, str]] = None,
) -> str:
    sql_str = _PipelineBuilder(
        pipeline=pipeline,
        data_sources=data_sources,
        transformations=transformations,
        mock_sql_inputs=mock_sql_inputs,
        materialization_context=materialization_context,
    ).get_sql_string()

    return sqlparse.format(sql_str, reindent=True)


def generate_random_name() -> str:
    return secrets.token_hex(10)


@dataclass
class _NodeInput:
    name: str
    sql_str: str


# This class is for the Athena FeatureView pipelines
class _PipelineBuilder:
    # The value of an internal node in the Pipeline tree
    _VALUE_TYPE = Union[str, CONSTANT_TYPE, BaseMaterializationContext]

    def __init__(
        self,
        pipeline: Pipeline,
        data_sources: List[specs.DataSourceSpec],
        transformations: List[specs.TransformationSpec],
        mock_sql_inputs: Optional[Dict[str, str]],
        materialization_context: BaseMaterializationContext,
    ):
        self._pipeline = pipeline
        self._id_to_ds = {ds.id: ds for ds in data_sources}
        self._id_to_transformation = {transform.id: transform for transform in transformations}
        self._mock_sql_inputs = mock_sql_inputs
        self._materialization_context = materialization_context
        self._ds_to_sql_str = {}

    def get_sql_string(self) -> str:
        sql_with_ds_vars = self._node_to_value(self._pipeline.root)
        assert isinstance(sql_with_ds_vars, str)

        # Define CTEs for the data sources before the SQL query.
        return DATA_SOURCE_TEMPLATE.render(data_sources=self._ds_to_sql_str, source=sql_with_ds_vars)

    def _node_to_value(self, pipeline_node: PipelineNode) -> _VALUE_TYPE:
        if pipeline_node.HasField("transformation_node"):
            return self._transformation_node_to_value(pipeline_node.transformation_node)
        elif pipeline_node.HasField("data_source_node"):
            return self._data_source_node_to_value(pipeline_node.data_source_node)
        elif pipeline_node.HasField("constant_node"):
            return constant_node_to_value(pipeline_node.constant_node)
        elif pipeline_node.HasField("materialization_context_node"):
            return self._materialization_context
        elif pipeline_node.HasField("request_data_source_node"):
            raise TectonValidationError("RequestDataSource is not supported in Athena FeatureView pipeline")
        elif pipeline_node.HasField("feature_view_node"):
            raise TectonValidationError("Dependent FeatureViews are not supported in Athena FeatureView pipeline")
        else:
            raise KeyError(f"Unknown PipelineNode type: {pipeline_node}")

    def _data_source_node_to_value(self, ds_node: DataSourceNode) -> str:
        """
        Returns a SQL string identifying the data source query (generated from the DS and a time window).
        If the returned value is a CTE name, the `_ds_to_sql_str` atribute is updated to map the CTE name
        to the underlying SQL query.
        """
        if self._mock_sql_inputs is not None and ds_node.input_name in self._mock_sql_inputs:
            return f"({self._mock_sql_inputs[ds_node.input_name]})"

        time_window = get_time_window_from_data_source_node(
            feature_time_limits=pendulum.period(
                self._materialization_context.start_time, self._materialization_context.end_time
            ),
            schedule_interval=self._materialization_context.batch_schedule,
            data_source_node=ds_node,
        )
        data_source = self._id_to_ds[IdHelper.to_string(ds_node.virtual_data_source_id)]
        return self._get_ds_sql_str(data_source, time_window)

    def _get_ds_sql_str(self, data_source: specs.DataSourceSpec, time_window: Optional[pendulum.Period]) -> str:
        hive_ds = data_source.batch_source
        if not hive_ds:
            raise TectonValidationError(f"Batch data source not found for: {data_source}")
        if not isinstance(hive_ds, specs.HiveSourceSpec):
            raise TectonValidationError(f"Athena FeatureViews do not support non-Hive batch data source: {hive_ds}")

        assert hive_ds.database and hive_ds.table
        # The database/table names are in the quotation marks to handle the scenario when they start with digits.
        ds_expression = f'"{hive_ds.database}"."{hive_ds.table}"'

        # If we have a time window, we need to filter the source based on it
        if time_window is not None:
            if not hive_ds.timestamp_field:
                raise TectonInternalError(
                    f"The `timestamp_field` must be set to use the data source time filtering for: {hive_ds}."
                )

            #  TODO(amargvela): pass in the partition filters when available.
            sql_str = TIME_LIMIT_TEMPLATE.render(
                select_columns=None,
                source=ds_expression,
                timestamp_key=hive_ds.timestamp_field,
                start_time=time_window.start,
                end_time=time_window.end,
            )
        else:
            sql_str = f"SELECT * FROM ({ds_expression})"

        cte_name = f"{TEMP_DS_PREFIX}_{generate_random_name()}"
        self._ds_to_sql_str[cte_name] = sql_str
        return cte_name

    def _transformation_node_to_value(self, transformation_node: TransformationNode) -> str:
        """Recursively translates inputs to values and then passes them to the transformation."""
        args = []
        kwargs = {}
        for transformation_input in transformation_node.inputs:
            node_value = self._node_to_value(transformation_input.node)
            if transformation_input.HasField("arg_index"):
                assert len(args) == transformation_input.arg_index
                args.append(node_value)
            elif transformation_input.HasField("arg_name"):
                kwargs[transformation_input.arg_name] = node_value
            else:
                raise KeyError(f"Unknown argument type for the Input node: {transformation_input}")

        return self._apply_transformation_function(transformation_node, args, kwargs)

    def _apply_transformation_function(self, transformation_node, args, kwargs) -> str:
        """For a given transformation node, returns the corresponding SQL string."""
        transformation = self._id_to_transformation[IdHelper.to_string(transformation_node.transformation_id)]
        user_function = transformation.user_function

        if transformation.transformation_mode == TransformationMode.TRANSFORMATION_MODE_ATHENA:
            return self._wrap_sql_function(transformation_node, user_function)(*args, **kwargs)
        else:
            raise KeyError(
                f"Invalid transformation mode: {TransformationMode.Name(transformation.transformation_mode)} for Athena FeatureView pipeline"
            )

    def _wrap_sql_function(
        self, transformation_node: TransformationNode, user_function: Callable[..., str]
    ) -> Callable[..., str]:
        def wrapped(*args, **kwargs):
            inputs = []
            wrapped_args = []
            for value, input_node in zip(args, positional_inputs(transformation_node)):
                input_value, is_transform_input = self._wrap_node_input_value(input_node, value)
                if is_transform_input:
                    cte_name = f"{TEMP_CTE_PREFIX}{generate_random_name()}"
                    wrapped_args.append(cte_name)
                    inputs.append(_NodeInput(name=cte_name, sql_str=input_value))
                else:
                    wrapped_args.append(input_value)

            keyword_inputs = get_keyword_inputs(transformation_node)
            wrapped_kwargs = {}
            for key, value in kwargs.items():
                input_node = keyword_inputs[key]
                input_value, is_transform_input = self._wrap_node_input_value(input_node, value)
                if is_transform_input:
                    cte_name = f"{TEMP_CTE_PREFIX}{key}"
                    wrapped_kwargs[key] = cte_name
                    inputs.append(_NodeInput(name=cte_name, sql_str=input_value))
                else:
                    wrapped_kwargs[key] = input_value

            user_function_sql = dedent(user_function(*wrapped_args, **wrapped_kwargs))
            sql_str = PIPELINE_TEMPLATE.render(inputs=inputs, user_function=user_function_sql)
            transformation_name = self._id_to_transformation[
                IdHelper.to_string(transformation_node.transformation_id)
            ].name
            transformation_type_checker(transformation_name, sql_str, "athena", self._possible_modes())
            return sql_str

        return wrapped

    def _wrap_node_input_value(self, input_node, value: _VALUE_TYPE) -> Tuple[Union[CONSTANT_TYPE], bool]:
        """
        Returns the node value, along with a boolean indicating whether the input is a SQL string of
        an upstream transformation.
        """
        if input_node.node.HasField("constant_node"):
            assert value is None or isinstance(value, CONSTANT_TYPE_OBJECTS)
            return value, False
        elif input_node.node.HasField("data_source_node"):
            assert isinstance(value, str)
            return value, False
        elif input_node.node.HasField("materialization_context_node"):
            assert isinstance(value, BaseMaterializationContext)
            return value, False
        else:
            # This should be a SQL string already, we need to return it wrapped in a parenthesis.
            assert isinstance(value, str)
            return f"({value})", True

    def _possible_modes(self):
        return ["athena", "pipeline"]


class _ODFVPipelineBuilder:
    def __init__(
        self,
        name: str,
        pipeline: Pipeline,
        transformations: List[specs.TransformationSpec],
    ):
        self._pipeline = pipeline
        self._name = name
        self._id_to_transformation = {t.id: t for t in transformations}
        self.mode = (
            "python"
            if self._id_to_transformation[
                IdHelper.to_string(self._pipeline.root.transformation_node.transformation_id)
            ].transformation_mode
            == TransformationMode.TRANSFORMATION_MODE_PYTHON
            else "pandas"
        )

    def _apply_transformation_function(self, transformation_node, args, kwargs) -> Union[Dict[str, Any], pd.DataFrame]:
        """For the given transformation node, returns the corresponding DataFrame transformation."""
        transformation = self._id_to_transformation[IdHelper.to_string(transformation_node.transformation_id)]
        user_function = transformation.user_function

        if transformation.transformation_mode == TransformationMode.TRANSFORMATION_MODE_PANDAS:
            try:
                res = user_function(*args, **kwargs)
            except Exception as e:
                raise UDF_ERROR(e)
            transformation_type_checker(transformation.name, res, "pandas", self._possible_modes())
            return res
        elif transformation.transformation_mode == TransformationMode.TRANSFORMATION_MODE_PYTHON:
            try:
                res = user_function(*args, **kwargs)
            except Exception as e:
                raise UDF_ERROR(e)
            # Only restrict types on the root node of python-mode transforms
            if transformation_node == self._pipeline.root:
                transformation_type_checker(transformation.name, res, "python", self._possible_modes())
            return res
        else:
            raise KeyError(f"Unknown transformation mode: {transformation.transformation_mode}")

    def _transformation_node_to_online_dataframe(
        self, transformation_node: TransformationNode
    ) -> Union[Dict[str, Any], pd.DataFrame]:
        """Recursively translates inputs to values and then passes them to the transformation."""
        args: List[Union[str, int, float, bool]] = []
        kwargs = {}
        for transformation_input in transformation_node.inputs:
            node_value = self._udf_node_to_value(transformation_input.node)
            if transformation_input.HasField("arg_index"):
                assert len(args) == transformation_input.arg_index
                args.append(node_value)
            elif transformation_input.HasField("arg_name"):
                kwargs[transformation_input.arg_name] = node_value
            else:
                raise KeyError(f"Unknown argument type for Input node: {transformation_input}")

        return self._apply_transformation_function(transformation_node, args, kwargs)

    # evaluate a node in the Pipeline
    def _udf_node_to_value(
        self, pipeline_node: PipelineNode
    ) -> Union[str, int, float, bool, None, Dict[str, Any], pd.DataFrame, pd.Series]:
        if pipeline_node.HasField("constant_node"):
            return constant_node_to_value(pipeline_node.constant_node)
        elif pipeline_node.HasField("feature_view_node"):
            if pipeline_node.feature_view_node.input_name not in self._passed_in_inputs:
                raise ValueError(
                    f"Expected to find input {pipeline_node.feature_view_node.input_name} in provided ODFV pipeline inputs"
                )

            return self._passed_in_inputs[pipeline_node.feature_view_node.input_name]
        elif pipeline_node.HasField("request_data_source_node"):
            if pipeline_node.request_data_source_node.input_name not in self._passed_in_inputs:
                raise ValueError(
                    f"Expected to find input {pipeline_node.feature_view_node.input_name} in provided ODFV pipeline inputs"
                )

            return self._passed_in_inputs[pipeline_node.request_data_source_node.input_name]
        elif pipeline_node.HasField("transformation_node"):
            return self._transformation_node_to_online_dataframe(pipeline_node.transformation_node)
        elif pipeline_node.HasField("materialization_context_node"):
            raise ValueError("MaterializationContext is unsupported for pandas pipelines")
        else:
            raise NotImplementedError("This is not yet implemented")

    def _possible_modes(self):
        # note that pipeline is included since this is meant to be a user hint, and it's
        # theoretically possible a pipeline wound up deeper than expected
        return ["pandas", "pipeline", "python"]

    def execute_with_inputs(self, inputs: Dict[str, pd.DataFrame]):
        self._passed_in_inputs = inputs
        return self._udf_node_to_value(self._pipeline.root)


def build_odfv_execution_pipeline(
    pipeline: Pipeline,
    transformations: List[specs.TransformationSpec],
    name: str,
) -> _ODFVPipelineBuilder:
    return _ODFVPipelineBuilder(
        name=name,
        pipeline=pipeline,
        transformations=transformations,
    )
