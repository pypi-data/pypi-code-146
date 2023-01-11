import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

DEFAULT_TIMESTAMP_TYPE = pa.timestamp("us")


def parquet_to_arrow(parquet: bytes) -> pa.Table:
    """Convert parquet as bytes to pyarrow table"""
    return pq.read_table(pa.py_buffer(parquet))


def arrow_to_parquet(table: pa.Table) -> bytes:
    """Convert pyarrow table to parquet as bytes"""
    buf = pa.BufferOutputStream()
    pq.write_table(table, buf)
    return buf.getvalue().to_pybytes()


def pandas_to_arrow(
    df: pd.DataFrame, schema: dict = None, preserve_index: bool = False
) -> pa.Table:
    if schema:
        arrow_schema = pa.schema(schema)
    else:
        arrow_schema = None

    table = pa.Table.from_pandas(df, arrow_schema, preserve_index=preserve_index)

    # pandas may leave metadata, which we don't want
    table = table.replace_schema_metadata(None)

    # cast timestamp columns to the default timestamp type
    new_fields = []
    for field in table.schema:
        if isinstance(field.type, pa.TimestampType):
            field = pa.field(
                field.name, pa.timestamp(DEFAULT_TIMESTAMP_TYPE.unit, tz=field.type.tz)
            )
        new_fields.append(field)
    new_schema = pa.schema(new_fields)
    table = table.cast(new_schema)

    return table


def arrow_to_pandas(table: pa.Table):
    df = table.to_pandas()
    return df


def pandas_to_parquet(df: pd.DataFrame, schema: dict = None) -> bytes:
    table = pandas_to_arrow(df, schema)
    return arrow_to_parquet(table)


def parquet_to_pandas(parquet: bytes) -> pd.DataFrame:
    table = parquet_to_arrow(parquet)
    return arrow_to_pandas(table)
