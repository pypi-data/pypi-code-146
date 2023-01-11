from typing import Dict

import attrs

from tecton_core import schema
from tecton_core.data_types import DataType
from tecton_proto.args import pipeline_pb2
from tecton_spark import schema_spark_utils
from tecton_spark.spark_schema_wrapper import SparkSchemaWrapper


@attrs.frozen
class RequestContext:
    """
    Wrapper around the RequestContext proto object (that is part of the RequestDataSourceNode in the FV pipeline).
    """

    schema: Dict[str, DataType]

    @classmethod
    def from_proto(cls, proto: pipeline_pb2.RequestContext) -> "RequestContext":
        wrapper = SparkSchemaWrapper.from_proto(proto.schema)
        schema = schema_spark_utils.schema_from_spark(wrapper.unwrap())
        return RequestContext(schema=schema.to_dict())

    def merge(self, other):
        for field in other.schema:
            if field in self.schema:
                assert self.schema[field] == other.schema[field], f"Mismatched request context field types for {field}"
            else:
                self.schema[field] = other.schema[field]
