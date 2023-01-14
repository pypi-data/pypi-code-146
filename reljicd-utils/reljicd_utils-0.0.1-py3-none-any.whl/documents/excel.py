from typing import Generator

import pandas
from pandas import notnull


def excel_itertuple_generator(file: str,
                              print_progress: bool = False) -> Generator:
    df = pandas.read_excel(file)
    df = df.where((notnull(df)),
                  None)  # Fix for converting NaN in dataframe to None

    total = df.shape[0] - 1

    for i, itertuple in enumerate(df.itertuples(), 1):
        if print_progress and not i % 1000:
            print(f'Finished inserting {i}/{total}')

        yield itertuple
