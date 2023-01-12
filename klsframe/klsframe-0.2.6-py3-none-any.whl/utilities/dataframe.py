from typing import Union

import pandas as pd
import re


def get_df_rows(df, rindex=None):
    """
    Get the specified rows of a Pandas data frame
    :param df: Pandas dataframe to be scrapped
    :param rindex: Index of the rows to retrieve. It accepts strings and integer numbers. Accepted:
        - None (default): all the rows are retrieved
        - 1: single number, single index
        - 1-4: indexes from 1 to 4, included
        - 2,3,4: indexes 2,3,4
        - 2,3,7-9: combination of the two previous modes
        - head-N: first N rows
        - tail-N: last N rows
        - first: acronym for head-1
        - last: acronym for tail-1
    :return: a list containing one dict per each row (the dict's keys are the column names, its values the row values)
    """
    data = []
    if rindex is None:
        data = []
        for index, row in df.iterrows():
            data.append({k: v for k, v in row.items()})
    elif isinstance(rindex, int):
        data = []
        for index, row in df.iterrows():
            if index == rindex:
                # data.append({k: v for k, v in row.items()})
                return {k: v for k, v in row.items()}
    else:
        rindex = str(rindex)
        if rindex == 'first':
            return get_df_rows(df, df.first_valid_index())
        elif rindex == 'last':
            return get_df_rows(df, df.last_valid_index())
        elif re.fullmatch('head-[0-9]+', rindex):
            rindex = range(df.first_valid_index(), int(rindex.split('-')[1]))
        elif re.fullmatch('tail-[0-9]+', rindex):
            rindex = range(df.last_valid_index() + 1 - int(rindex.split('-')[1]), df.last_valid_index() + 1)
        elif re.fullmatch('[0-9]+-[0-9]+', rindex):
            rindex = range(int(rindex.split('-')[0]), int(rindex.split('-')[1]) + 1)
        elif re.fullmatch('([0-9](-[0-9]+)?,)*[0-9]+(-[0-9]+)?', rindex):
            # rindex = [int(i) for i in rindex.split(',')]
            aux = []
            for i in rindex.split(','):
                try:
                    aux.append(int(i))
                except ValueError:
                    aux.extend(range(int(i.split('-')[0]), int(i.split('-')[1]) + 1))
            rindex = aux
        else:
            raise ValueError("Unexpected value for parameter 'rindex'")

        for index, row in df.iterrows():
            if index in rindex:
                data.append({k: v for k, v in row.items()})
    return data


def df_add_column(dataframe, col, on, how='left') -> pd.DataFrame:
    return dataframe.merge(col, on=on, how=how)


def df_to_excel(output_file, contents: Union[dict, pd.DataFrame]) -> None:
    """
    Saves the contents of a dataframe into an Excel file.

    contents_example = {
        'MasterNmap': df,
        'Metrics_Ports': df_statistics_master,
        'Metrics_Ports_2': df_IPs_StatusPorts,
        'Sum_OpenPorts': df_summary_openports,
        'Sum_ClosedPorts': df_summary_closedports,
        'SumFilteredPorts': df_summary_filteredports
    }
    :param output_file: name for the Excel file
    :param contents: single DataFrame or a dictionary,
        whose keys are page names, and its values the corresponding dataframe
    :return: None
    """
    if isinstance(contents, dict):
        with pd.ExcelWriter(f"{output_file}.xlsx") as writer:
            for sheet_name, dataframe in contents.items():
                dataframe.to_excel(writer, sheet_name=str(sheet_name), index=False, header=True)
    elif isinstance(contents, pd.DataFrame):
        with pd.ExcelWriter(f"{output_file}.xlsx") as writer:
            contents.to_excel(writer, index=False, header=True)
    else:
        raise TypeError("Invalid type for paramterer 'mapping'. Expected: dict|DataFrame")
