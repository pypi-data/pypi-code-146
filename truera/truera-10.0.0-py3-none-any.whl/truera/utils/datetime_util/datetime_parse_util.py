import datetime
from typing import Optional

import pandas as pd

# Separate util from datetime_helper because it uses pandas which is not available in CLI (and is
# only there becuse other utils are used from that file.)


def get_datetime_from_string(time_string: str) -> datetime.datetime:
    return pd.to_datetime(time_string).to_pydatetime()


def get_datetime_from_proto_string(
    time_string: Optional[str]
) -> datetime.datetime:
    return get_datetime_from_string(
        time_string
    ) if time_string else datetime.datetime.min


def parse_timestamp_from_dataframe(
    dataframe: pd.DataFrame, timestamp_column_name: str,
    include_timestamp_col: bool
):
    if include_timestamp_col:
        # get datetime from integer epoch, but cast to string for AIQ purposes
        dataframe[timestamp_column_name] = pd.to_datetime(
            dataframe[timestamp_column_name], unit="s"
        ).astype(str)
    else:
        dataframe = dataframe.drop([timestamp_column_name], axis="columns")
    return dataframe
