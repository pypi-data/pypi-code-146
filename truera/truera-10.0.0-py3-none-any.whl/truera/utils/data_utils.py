from typing import List, Optional, Sequence

import numpy as np
import pandas as pd

import truera.protobuf.public.aiq.intelligence_service_pb2 as is_pb
from truera.utils.truera_status import TruEraInternalError

MAX_UNIQUE_VALS_FOR_CATEGORICAL_FEATURES = 5


def update_value_table_from_dataframe(
    df: pd.DataFrame, value_table: is_pb.ValueTable
):
    for col, col_dtype in df.dtypes.iteritems():
        value_list = value_table.column_value_map[col]
        series = df[col]
        if pd.api.types.is_string_dtype(col_dtype):
            series = series.fillna("").astype(str)
            value_list.strings.values.extend(series.tolist())
        elif pd.api.types.is_integer_dtype(col_dtype):
            value_list.integers.values.extend(series.tolist())
        elif pd.api.types.is_numeric_dtype(col_dtype):
            value_list.floats.values.extend(series.tolist())
        else:
            raise TruEraInternalError(
                f"Could not find appropriate datatype to serialize column {col} of type {col_dtype}!"
            )
    try:
        #devnote: this will try to set the row_labels if index is there else just let it be without disrupting the flow
        index_list = df.index.tolist()
        value_table.row_labels.extend(index_list)
    except:
        pass


def update_float_table_from_dataframe(
    df: pd.DataFrame, float_table: is_pb.FloatTable
):
    for col in df.columns:
        float_list = float_table.column_value_map[col]
        float_list.values.extend(df[col].tolist())
    if df.index.name:
        float_table.row_labels.extend(df.index.tolist())


def update_string_table_from_dataframe(
    df: pd.DataFrame, string_table: is_pb.StringTable
):
    for col in df.columns:
        string_list = string_table.column_value_map[col]
        string_list.values.extend(df[col].tolist())
    if df.index.name:
        string_table.row_labels.extend(df.index.tolist())


def is_categorical_feature(feature_data: pd.Series) -> bool:
    return (not np.issubdtype(feature_data.dtype, np.number)) or (
        len(feature_data.unique()) <= MAX_UNIQUE_VALS_FOR_CATEGORICAL_FEATURES
    )


def value_table_to_df(
    value_table: is_pb.ValueTable,
    ordered_column_names: Optional[Sequence[str]] = None
):
    cvm = value_table.column_value_map
    cols = ordered_column_names if ordered_column_names else cvm.keys()
    mp = {col: get_list_from_value_list(cvm[col]) for col in cols}
    ret = pd.DataFrame(mp, columns=cols)
    row = value_table.row_labels
    if row:
        ret.index = row
    return ret


def string_table_to_df(
    string_table: is_pb.StringTable,
    ordered_column_names: Optional[Sequence[str]] = None
):
    cvm = string_table.column_value_map
    cols = ordered_column_names if ordered_column_names else cvm.keys()
    mp = {col: list(cvm[col].values) for col in cols}
    ret = pd.DataFrame(mp, columns=cols)
    row = string_table.row_labels
    if row:
        ret.index = row
    return ret


def value_table_to_df_or_series(
    value_table: is_pb.ValueTable,
    ordered_column_names: Optional[Sequence[str]] = None
):
    df = value_table_to_df(
        value_table, ordered_column_names=ordered_column_names
    )
    if df.shape[1] == 1:
        return df[df.columns[0]]
    return df


def float_table_to_df(float_table, ordered_column_names=None):
    cvm = float_table.column_value_map
    cols = ordered_column_names if ordered_column_names else cvm.keys()
    mp = {col: list(cvm[col].values) for col in cols}
    ret = pd.DataFrame(mp, columns=cols)
    row = float_table.row_labels
    if row:
        ret.index = row
    return ret


def get_list_from_value_list(value_list):
    has_strings = hasattr(value_list,
                          "strings") and len(value_list.strings.values) > 0
    has_integers = hasattr(value_list,
                           "integers") and len(value_list.integers.values) > 0
    if has_integers:
        ret = value_list.integers.values
    elif has_strings:
        ret = value_list.strings.values
    else:
        ret = value_list.floats.values
    return list(ret)


def merge_split_data_responses(
    responses: List[is_pb.SplitDataResponse]
) -> is_pb.SplitDataResponse:
    final_response = is_pb.SplitDataResponse()
    final_response.split_metadata.CopyFrom(responses[0].split_metadata)
    merge_value_tables(
        [resp.split_data for resp in responses], final_response.split_data
    )
    merge_value_tables(
        [resp.split_extra_data for resp in responses],
        final_response.split_extra_data
    )
    merge_value_tables(
        [resp.split_labels for resp in responses], final_response.split_labels
    )
    return final_response


def merge_value_tables(
    value_tables: List[is_pb.ValueTable], valueTable: is_pb.ValueTable
):
    value_tables_dfs = [value_table_to_df(table) for table in value_tables]
    merged_value_tables = pd.concat(value_tables_dfs)
    if not merged_value_tables.empty:
        update_value_table_from_dataframe(merged_value_tables, valueTable)
