from typing import Any, Union
import pandas as pd
from numpy import array
import time

__all__ = ["wait_until", "data_factory"]


def wait_until(somepredicate, timeout, period=1, *args, **kwargs):
    mustend = time.time() + timeout
    while time.time() < mustend:
        if somepredicate(*args, **kwargs):
            return True
        time.sleep(period)
    raise RuntimeError(
        f"Executing query exceed {timeout} seconds, please call query.wait_for_finish(timeout=int) to set a longer waiting time"
    )


def data_factory(data_format="list", **options) -> Union[pd.DataFrame, list, Any]:
    def get_df(columns, data):
        data_list = get_list(columns, data)
        # enforce to show the data frame dimesion e.g: [499 rows x 9 columns]
        pd.set_option("show_dimensions", True)
        return pd.DataFrame(data_list[1:], columns=data_list[0])

    def get_np(columns, data):
        return array(data)

    def get_list(columns, data, with_column=True):
        if with_column == True:
            column_names = list(map(lambda column: column["name"], columns))
            return [column_names] + data
        return data

    if data_format == "list":
        return get_list(**options)
    if data_format == "df":
        return get_df(**options)
    if data_format == "np":
        return get_np(**options)
    raise RuntimeError(f"Unexpected data_format {data_format}")
