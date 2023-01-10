import pandas as pd
from io import StringIO, BytesIO
from typing import Union, Optional
from ..os.file import check_file_exist


def read_csv(path: Union[str, BytesIO, StringIO], chunksize: Optional[int] = None, parse_dates: bool = False, date_parser: Optional[str] = None, keep_default_na: bool = True, na_values: Optional[list] = None, names: Optional[list] = None, sep: Optional[list] = None, true_values: Optional[list] = None, false_values: Optional[list] = None) -> list:
    results = []
    datas = pd.read_csv(path, chunksize=chunksize, low_memory=False, parse_dates=parse_dates, date_parser=date_parser, names=names, sep=sep, true_values=true_values, false_values=false_values, keep_default_na=keep_default_na, na_values=na_values)
    if chunksize is not None:
        for data in datas:
            for index, row in data.iterrows():
                results.append(row.to_dict())
    else:
        for index, row in datas.iterrows():
            results.append(row.to_dict())
    return results


def values_to_csv(values: dict, path: str, is_append: bool = False, is_transpose: bool = False,  **kwargs):
    mode = 'a' if is_append is True else 'w'
    if check_file_exist(path) is False:
        if is_transpose is False:
            pd.DataFrame(values).to_csv(path, mode=mode, encoding='utf-8', **kwargs)
        else:
            pd.DataFrame(values).T.to_csv(path, mode=mode, encoding='utf-8', **kwargs)
    else:
        if is_transpose is False:
            pd.DataFrame(values).to_csv(path, mode=mode, encoding='utf-8', **kwargs)
        else:
            pd.DataFrame(values).T.to_csv(path, mode=mode, encoding='utf-8', **kwargs)


def csv_to_values(path: str, is_transpose: bool = False,  **kwargs):
    results = []
    if check_file_exist(path) is True:
        datas = pd.read_csv(path, **kwargs) if is_transpose is False else pd.read_csv(path, **kwargs).T
        if 'chunksize' in kwargs.items():
            for data in datas:
                for index, row in data.iterrows():
                    results.append(row.to_dict())
        else:
            for index, row in datas.iterrows():
                results.append(row.to_dict())
    return results
