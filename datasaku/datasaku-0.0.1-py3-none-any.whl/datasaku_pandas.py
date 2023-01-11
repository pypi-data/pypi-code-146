""" pandas related module """

import pandas as pd
import importlib_resources
import io
import gzip
import csv

def pandas_country_iso3166(col_df_def, code_from_var_def, code_to_var_def):
    """
    Conversion country from code to name or vice versa.  
    Available conversion are: country,alpha_2,alpha_3,numeric,iso_3166-2  
    - col_df_def = the pandas dataframe column.
    - code_from_var_def = the origin before conversion.
    - code_to_var_def = the conversion that you want to have.
    """
    col_df_def = pd.DataFrame(col_df_def)
    my_resources = importlib_resources.files("beat_python")
    data = (my_resources / "data" / "country_code.csv").read_bytes()
    country_code = pd.read_csv(io.BytesIO(data), encoding='utf-8-sig')
    country_code['lower'] = country_code[code_from_var_def].str.lower()
    col_df_def['lower'] = col_df_def[col_df_def.columns[0]].str.lower()
    merge = col_df_def.merge(country_code, how = 'left', left_on = 'lower', right_on = 'lower')
    output = merge.loc[:, [code_to_var_def]]
    return output

def pandas_city_timezone(col_df_def):
    """
    Get timezone from city name. There will be cases that the output is nan which means that the city name is not match
    - col_df_def = the pandas dataframe column.
    """
    source = importlib_resources.files('beat_python.data').joinpath('geonames_higher_50000.csv.gz')
    with importlib_resources.as_file(source) as file:
        with gzip.open(file, mode="rt") as f:
            csvobj = pd.read_csv(f,delimiter = ',', encoding = 'utf-8-sig')
    timezone = csvobj
    timezone['lower'] = timezone['name'].str.lower()
    col_df_def = pd.DataFrame(col_df_def)
    col_df_def['lower'] = col_df_def[col_df_def.columns[0]].str.lower()
    col_df_def_merge = col_df_def.merge(timezone.loc[:, ['lower', 'timezone']], how = 'left', left_on = 'lower', right_on = 'lower')
    output = col_df_def_merge.loc[:, ['timezone']]
    return output