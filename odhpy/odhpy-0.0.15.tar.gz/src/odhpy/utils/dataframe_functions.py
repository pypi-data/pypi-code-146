import pandas as pd
from odhpy import utils
from pandas.api.types import is_datetime64_any_dtype as is_datetime


def assert_df_format_standards(df: pd.DataFrame):
    """
    Args:
        df (pd.DataFrame): _description_
    """
    violations = check_df_format_standards(df)
    if len(violations) > 0:
        raise Exception(f"Dataframe does not meet odhpy format standards.\n {violations[0]}")
    

def check_df_format_standards(df: pd.DataFrame):
    """
    Checks if a given dataframe meets standards generally requried by 
    odhpy functions. These standards include:
    - Dataframe is not none
    - Dataframe index datatype is datetime
    - Dataframe index name is "Date"
    - Dataframe index values are daily sequential with no time-component
    - Data columns all have datatype of double
    - Missing values are nan (not na, not -nan)
    - Dataframe index name is

    Args:
        df (_type_): _description_

    Returns:
        bool: _description_
    """
    # - Dataframe is not none
    if df is None:
        return ["Dataframe is None"]
    # - Dataframe index datatype is datetime
    if not is_datetime(df.index):
        return ["Dataframe index type is not datetime"]
    # - Dataframe index name is "Date"
    if df.index.name != "Date":
        return ["Dataframe index name is not 'Date'"]
    # - Dataframe index values are daily sequential with no time-component
    start_date = min(df.index)
    expected_dates = utils.get_dates(start_date=start_date, days=len(df))
    for i in range(len(df)):
        if df.index.values[i] != expected_dates[i]:
            return [f"Unexpected datetime {df.index.values[i]} at index {i}"]
    # - Data columns all have datatype of double
    for c in df.columns:
        data_type = df[c].dtypes
        if (data_type != 'int64') and (df[c].dtypes != 'float64'):
            return [f"Column '{c}' is not int64 or float64: {data_type}"]
    # - Missing values are nan (not na, not -nan)
    # - Dataframe index name is
    return []



def set_index_dt(df: pd.DataFrame, dt_values=None, start_dt=None, cancel_if_index_are_datetimes=True, **kwargs):
    """
    Returns a dataframe with datetimes as the index.     
    If no optional arguments are provided, the function will look for a column named "Date" (not 
    case-sensitive) within the input dataframe. Otherwise dt_values or start_dt (assumes daily)
    may be provided. 

    Args:
        df (pd.DataFrame): _description_
        dt_values (_type_, optional): _description_. Defaults to None.
        start_dt (_type_, optional): _description_. Defaults to None.
        cancel_if_index_are_datetimes (bool, optional): _description_. Defaults to True.
    """
    if cancel_if_index_are_datetimes and is_datetime(df.index):
        return df
    
    if start_dt != None:
        df["Date"] = utils.get_dates(start_dt, days=len(df))    
    elif dt_values != None:
        nn = len(df)
        if len(dt_values) < nn:
            raise Exception("dt_values is shorter than the dataframe.") 
        df["Date"] = dt_values[:nn]
 
    col = [c for c in df.columns if c.upper().strip() == "DATE"]
    if len(col) > 0:
        df["Date"] = pd.to_datetime(df[col[0]], **kwargs)
        answer = df.set_index("Date")
        return answer
    else:
        raise Exception("Could not find 'Date' column.")
