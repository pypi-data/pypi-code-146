import base64 as b64

import pandas as pd
import pyarrow as pa

from warpzone.transform import data


def msg_body_to_arrow(msg_body: bytes) -> pa.Table:
    return data.parquet_to_arrow(b64.b64decode(msg_body))


def msg_body_to_pandas(msg_body: bytes) -> pd.DataFrame:
    return data.parquet_to_pandas(b64.b64decode(msg_body))


def arrow_to_msg_body(table: pa.Table) -> bytes:
    return b64.b64encode(data.arrow_to_parquet(table))


def pandas_to_msg_body(df: pd.DataFrame, schema: dict = None) -> bytes:
    return b64.b64encode(data.pandas_to_parquet(df, schema))
