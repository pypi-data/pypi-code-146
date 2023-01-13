import pandas as pd
import copy
from ..tools import DataFrameTools as DfTools


# ExcelDf: Class to store dataframe sources for a generic source
class AbsSourceDf():
    """
     An abstract class to store extra meta information regarding a `DataFrame`_

     Attributes
     ----------
     df: `DataFrame`_
        The source data table
    """
    def __init__(self, df: pd.DataFrame):
        self.df = df
