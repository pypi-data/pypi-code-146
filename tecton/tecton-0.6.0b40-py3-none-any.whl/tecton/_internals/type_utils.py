from typing import List

from pyspark.sql import types as spark_types

from tecton.types import Field
from tecton_proto.common import schema_pb2
from tecton_spark.spark_schema_wrapper import SparkSchemaWrapper


def to_column(field: Field) -> schema_pb2.Column:
    data_type = field.tecton_type().proto.data_type
    return schema_pb2.Column(name=field.name, offline_data_type=data_type)


def to_tecton_schema(fields: List[Field]) -> schema_pb2.Schema:
    columns = [to_column(field) for field in fields]
    return schema_pb2.Schema(columns=columns)


def to_spark_schema_wrapper(field_list: List[Field]) -> SparkSchemaWrapper:
    s = spark_types.StructType([field.spark_type() for field in field_list])
    return SparkSchemaWrapper(s)
