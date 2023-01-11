import os
import numpy as np
import pandas as pd
from datetime import datetime
import uuid
import shutil
import subprocess
from odhpy import utils
na_values = ['', ' ', 'null', 'NULL', 'NAN', 'NaN', 'nan', 'NA', 'na', 'N/A' 'n/a', '#N/A', '#NA', '-NaN', '-nan']


def read_iqqm_lqn_output(filename, col_name=None, df=None) -> pd.DataFrame:
    """Reads the output of IQQM listquan. This is format is the same for flows and diversions.

    Args:
        filename (_type_): _description_
        df (_type_, optional): _description_. Defaults to None.

    Returns:
        pd.DataFrame: _description_
    """
    # If no df was supplied, instantiate a new one
    if df is None:
        df = pd.DataFrame()
    # If no column name was specified, we use the base name of the file
    if col_name is None:
        col_name = os.path.basename(filename)
    # Read the data
    data_start_row=7
    temp = pd.read_csv(filename, skiprows=(data_start_row-2), delim_whitespace=True, names=["Date", col_name], header=None)
    temp = utils.set_index_dt(temp, format='%d/%m/%Y')
    temp = temp.replace(r'^\s*$', np.nan, regex=True)
    df = df.join(temp, how="outer").sort_index()
    # TODO: THERE IS NO GUARANTEE THAT THE DATES OVERLAP, THEREFORE WE MAY END UP WITH A DATAFRAME WITH INCOMPLETE DATES
    # TODO: I SHOULD MAKE DEFAULT BEHAVIOUR AUTO-DETECT FORMAT DEPENDING ON *TYPE* AND *LOCATION* OF DELIMIT CHARS
    # TODO: In the meantime we use the below to assert that the format of the resulting df meets our minimum standards.
    utils.assert_df_format_standards(df)
    return df
    
    
def read_ts_csv(filename, date_format=r"%d/%m/%Y", df=None, colprefix="", **kwargs):
    """Reads a daily timeseries csv into a DataFrame, and sets the index to the Date.
    Assumed there is a column named "Date"

    Args:
        filename (_type_): _description_
        date_format (str, optional): defaults to "%d/%m/%Y" as per Fors. Other common formats include "%Y-%m-%d", "%Y/%m/%d".

    Returns:
        _type_: _description_
    """
    # If no df was supplied, instantiate a new one
    if df is None:
        df = pd.DataFrame()
    # Read the data
    temp = pd.read_csv(filename, na_values=na_values, **kwargs)
    temp = utils.set_index_dt(temp, format=date_format)
    temp = temp.replace(r'^\s*$', np.nan, regex=True)
    if colprefix is not None:
        for c in temp.columns:
            temp.rename(columns = {c:f"{colprefix}{c}"}, inplace = True)        
    df = df.join(temp, how="outer").sort_index()
    # TODO: THERE IS NO GUARANTEE THAT THE DATES OVERLAP, THEREFORE WE MAY END UP WITH A DATAFRAME WITH INCOMPLETE DATES
    # TODO: I SHOULD MAKE DEFAULT BEHAVIOUR AUTO-DETECT FORMAT DEPENDING ON *TYPE* AND *LOCATION* OF DELIMIT CHARS
    # TODO: In the meantime we use the below to assert that the format of the resulting df meets our minimum standards.
    utils.assert_df_format_standards(df)
    return df


def write_area_ts_csv(df, filename, units = "(mm.d^-1)"):
    """_summary_

    Args:
        df (_type_): _description_
        filename (_type_): _description_
        units (str, optional): _description_. Defaults to "(mm.d^-1)".

    Raises:
        Exception: If shortenned field names are going to clash in output file.
    """
    # ensures dataframe has daily datetime index
    df = utils.set_index_dt(df) 
    # convert field names to 12 chars and check for collisions
    fields = {}
    for c in df.columns:
        c12 = f"{c[:12]:<12}"
        if c12 in fields.keys():
            raise Exception(f"Field names clash when shortenned to 12 chars: {c} and {fields[c12]}")
        fields[c12] = c
    # create the header text
    header = f"{units}"
    for k in fields.keys():
        header += f',"{k}"'
    header += os.linesep
    header += "Catchment area (km^2)"
    for k in fields.keys():
        header += f", 1.00000000"
    header += os.linesep
    # open a file and write the header and the csv body
    with open(filename, "w+", newline='', encoding='utf-8') as file:        
        file.write(header)
        df.to_csv(file, header=False, na_rep=' NaN')
        
        
def write_idx(df, filename, cleanup_tempfile=True):
    """_summary_

    Args:
        df (_type_): _description_
        filename (_type_): _description_
    """
    if shutil.which('csvidx') is None:
        raise Exception("This method relies on the external program 'csvidx.exe'. Please ensure it is in your path.")
    temp_filename = f"{uuid.uuid4().hex}.tempfile.csv"
    write_area_ts_csv(df, temp_filename)
    command = f"csvidx {temp_filename} {filename}"
    process = subprocess.Popen(command)
    process.wait()
    if cleanup_tempfile:
        os.remove(temp_filename)
    
