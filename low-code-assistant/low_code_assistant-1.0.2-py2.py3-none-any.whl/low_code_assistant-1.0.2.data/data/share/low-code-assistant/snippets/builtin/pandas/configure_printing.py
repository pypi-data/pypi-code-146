# author: Maarten Breddels
# date: Wed 8 Sep 2022
# requires pandas:
#  pip install pandas
import pandas as pd

# set to very low values to demonstrate the effect of the settings
# for all settings, see https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.set_option.html
pd.set_option("display.max_rows", 5)
pd.set_option("display.max_columns", 2)
pd.set_option("display.precision", 2)
