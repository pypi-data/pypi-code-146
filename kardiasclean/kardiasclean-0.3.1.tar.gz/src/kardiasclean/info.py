"""Utility functions to get insight on a DataFrame."""
import pandas as pd


def get_unique_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Get the total unique values in all columns.

    Args:
        df (pd.DataFrame): Column.

    Returns:
        int: Count number.
    """
    unique = pd.DataFrame(
        {column: df[column].value_counts().count() for column in df.columns},
        index=["unique_count"],
    )
    percent = (unique / df.count()).rename(index={"unique_count": "percent_of_total"})
    per = (1 / percent).rename(index={"percent_of_total": "avg_per_record"})
    return pd.concat(
        [
            unique,
            percent,
            per,
        ]
    )


def get_difference_index(a: pd.DataFrame, b: pd.DataFrame) -> pd.DataFrame:
    """Get the index values from dataframe "a" that don't exist in dataframe "b".

    Args:
        a (pd.DataFrame): Dataframe with the most values.
        b (pd.DataFrame): Dataframe with the least values.

    Returns:
        pd.DataFrame: Index that can be used to index the original dataframe.
    """
    return list(set(a.index) - set(b.index))


def evaluate_distribution(high_frequency: pd.Series, low_frequency: pd.Series) -> str:
    """Given two value counts arrays, print a summary of the distribution.

    Args:
        high_frequency (pd.Series): Data.
        low_frequency (pd.Series): Data.

    Returns:
        str: String to print.
    """
    n_other = low_frequency.sum()
    n_top = high_frequency.sum()
    count_top = high_frequency.count()
    total = n_other + n_top
    return (
        f"Total data (repeated): {total}\n"
        f"{'-'*20}\n"
        f"Unique high frequency data: {high_frequency.count()}\n"
        f"Unique low frequency data: {low_frequency.count()}\n"
        f"{'-'*20}\n"
        f"Total high frequency data: {n_top}\n"
        f"Total low frequency data: {n_other}\n"
        f"{'-'*20}\n"
        f"Percentage of high data: {100*n_top/total:.2f}%\n"
        f"Percentage of low data: {100*n_other/total:.2f}%\n"
        f"{'-'*20}\n"
        f"Summary\n"
        f"{'-'*20}\n"
        f"From {total} data, there are {count_top} unique records\n" 
        f"that account for {100*n_top/total:.2f}% of the total data (repeated).\n"
    )
