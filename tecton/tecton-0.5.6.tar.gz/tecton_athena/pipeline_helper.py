from typing import Any
from typing import Dict
from typing import List
from typing import Union

import pandas as pd

from tecton_core import function_deserialization
from tecton_core.errors import UDF_ERROR
from tecton_core.id_helper import IdHelper
from tecton_core.pipeline_common import constant_node_to_value
from tecton_core.pipeline_common import get_transformation_name
from tecton_core.pipeline_common import transformation_type_checker
from tecton_proto.args.new_transformation_pb2 import TransformationMode
from tecton_proto.args.pipeline_pb2 import Pipeline
from tecton_proto.args.pipeline_pb2 import PipelineNode
from tecton_proto.args.pipeline_pb2 import TransformationNode
from tecton_proto.data.new_transformation_pb2 import NewTransformation as Transformation


class _ODFVPipelineBuilder:
    def __init__(
        self,
        name: str,
        pipeline: Pipeline,
        transformations: List[Transformation],
    ):
        self._pipeline = pipeline
        self._name = name
        self._id_to_transformation = {IdHelper.to_string(t.transformation_id): t for t in transformations}
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
        user_function = function_deserialization.from_proto(transformation.user_function)
        transformation_name = get_transformation_name(transformation)

        if transformation.transformation_mode == TransformationMode.TRANSFORMATION_MODE_PANDAS:
            try:
                res = user_function(*args, **kwargs)
            except Exception as e:
                raise UDF_ERROR(e)
            transformation_type_checker(transformation_name, res, "pandas", self._possible_modes())
            return res
        elif transformation.transformation_mode == TransformationMode.TRANSFORMATION_MODE_PYTHON:
            try:
                res = user_function(*args, **kwargs)
            except Exception as e:
                raise UDF_ERROR(e)
            # Only restrict types on the root node of python-mode transforms
            if transformation_node == self._pipeline.root:
                transformation_type_checker(transformation_name, res, "python", self._possible_modes())
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
    transformations: List[Transformation],
    name: str,
) -> _ODFVPipelineBuilder:
    return _ODFVPipelineBuilder(
        name=name,
        pipeline=pipeline,
        transformations=transformations,
    )
