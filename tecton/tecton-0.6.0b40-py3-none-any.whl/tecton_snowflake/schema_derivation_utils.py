import json

from tecton_proto.args import data_source_pb2
from tecton_proto.args import virtual_data_source_pb2
from tecton_proto.common import spark_schema_pb2
from tecton_snowflake.utils import format_sql


def get_data_source_schema_sql(ds_args: data_source_pb2.SnowflakeDataSourceArgs) -> str:
    """Return the SQL used to query the data source provided."""
    if ds_args.HasField("table"):
        full_table_name = f"{ds_args.database}.{ds_args.schema}.{ds_args.table}"
        sql_str = f"SELECT * FROM {full_table_name};"
    elif ds_args.HasField("query"):
        sql_str = f"{ds_args.query}"
    else:
        raise ValueError("A Snowflake source must have one of 'query' or 'table' set")
    return format_sql(sql_str)


def get_snowflake_schema(
    ds_args: virtual_data_source_pb2.VirtualDataSourceArgs, connection: "snowflake.connector.Connection"
) -> spark_schema_pb2.SparkSchema:
    """Derive schema for snowflake data source on snowflake compute.

    This method is used for notebook driven development.
    The logic should mirror logic in resolveBatch() in SnowflakeDDL.kt.
    """
    cur = connection.cursor()

    sql_str = get_data_source_schema_sql(ds_args.snowflake_ds_config)
    cur.execute(sql_str)
    # Get the schema from the previously ran query
    query_id = cur.sfqid
    cur.execute(f"DESCRIBE RESULT '{query_id}';")
    schema_list = cur.fetchall()  # TODO: use fetch_pandas_all() once it supports describe statements

    proto = spark_schema_pb2.SparkSchema()
    for row in schema_list:
        # schema returned is in the form (name, type,...)
        name = row[0]
        proto_field = proto.fields.add()
        proto_field.name = name
        proto_field.structfield_json = json.dumps({"name": name, "type": row[1], "nullable": True, "metadata": {}})
    return proto
