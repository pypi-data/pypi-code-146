from typing import Dict, Generator

import numpy
import pandas
from pandas import notnull


def csv_dict_generator(
        file: str,
        separator: str = ",",
        encoding: str = "utf-8",
        error_bad_lines: bool = True) -> Generator[Dict, None, None]:
    df = pandas.read_csv(file, sep=separator, encoding=encoding,
                         error_bad_lines=error_bad_lines)
    df = df.where((notnull(df)),
                  None)  # Fix for converting NaN in dataframe to None

    for original_record in df.to_dict('records'):
        record = {}
        for key, value in original_record.items():
            if isinstance(value, numpy.int64):  # Fix for psycopg
                value = int(value)
            record[key] = value

        yield record
