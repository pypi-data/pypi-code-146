import pandas as pd
from functools import reduce


def _rename_columns(df: pd.DataFrame):
    def _rename(col: str):
        should_replace = col.endswith('dataCompleteness.fertilizer')
        column = col.replace('dataCompleteness.fertilizer', 'dataCompleteness.fertiliser') if should_replace else col
        return {col: column}

    columns = list(df.columns)
    new_columns = reduce(lambda prev, curr: {**prev, **_rename(curr)}, columns, {})
    return df.rename(columns=new_columns)


def migrate(df: pd.DataFrame):
    return _rename_columns(df)
