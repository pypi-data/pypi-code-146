from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

import attrs

from tecton_core import pipeline_common
from tecton_core import specs
from tecton_core.id_helper import IdHelper
from tecton_core.materialization_context import BoundMaterializationContext
from tecton_proto.args.pipeline_pb2 import Pipeline
from tecton_proto.args.pipeline_pb2 import PipelineNode


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
            return pipeline_common.constant_node_to_value(pipeline_node.constant_node)
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


def unique_node_alias(node: PipelineNode) -> str:
    return f"node_{id(node)}"
