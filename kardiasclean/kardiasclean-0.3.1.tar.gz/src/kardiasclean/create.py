"""Create DataFrames from other dfs or columns."""
import pandas as pd


def spread_column(column: pd.Series) -> pd.DataFrame:
    """Returns a Column with values spread over duplicated indexes.

    If {1: [a, b], 2:[c]}, then the result will be {1:a, 1:b, 2:c}.

    Args:
        column (pd.Series): Column to spread.

    Returns:
        pd.DataFrame:

    Example:

        surgery_map = create_spread_column(df['surgery'])
    """
    return pd.DataFrame(
        [
            (index_i, values_j)
            for index_i, values_i in column.items()
            for values_j in values_i
        ],
        columns=[column.index.name, column.name],
    )


def create_unique_list(
    df: pd.DataFrame, column: pd.Series, position: int = 0
) -> pd.DataFrame:
    """Create a list of unique values in a dataframe from given column.

    Args:
        df (pd.DataFrame): Complete dataframe.
        column (pd.Series): Column.
        position (int, optional): Get first or last, 0 or -1. Defaults to 0.

    Returns:

        pd.DataFrame: New dataframe with non-repeated values.
    """
    return pd.DataFrame(
        [df[column == token].iloc[position] for token in column.unique()],
        columns=df.columns,
    ).reset_index().drop(["index"], axis=1)
