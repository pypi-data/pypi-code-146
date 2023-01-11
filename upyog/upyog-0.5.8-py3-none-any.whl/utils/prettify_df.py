"""
SOURCE: https://github.com/khuyentran1401/rich-dataframe/blob/master/rich_dataframe/rich_dataframe.py
Some minor modifications made re. color, caption, etc
"""

from tabulate import tabulate
from upyog.imports import *


def print_df(
    df: Union[pd.DataFrame, pd.Series],
    title: Optional[str] = None,
    headers = "keys", tablefmt = "psql",
    **tabulate_kwargs,
):
    if title:                     print(title)
    if isinstance(df, pd.Series): df = pd.DataFrame(df)

    table = tabulate(
        df,
        headers = headers,
        tablefmt = tablefmt,
        **tabulate_kwargs
    )
    print(table)

    return table

def print_df(df):
    from prettytable import PrettyTable

    if isinstance(df, pd.Series): df = pd.DataFrame(df)

    table = PrettyTable(max_width=50)
    table.field_names = df.columns  # Set the column names

    # Add the rows to the table
    for row in df.itertuples(index=False):
        table.add_row(row)

    print(table)
