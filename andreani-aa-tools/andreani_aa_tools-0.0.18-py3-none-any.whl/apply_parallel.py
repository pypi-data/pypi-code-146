import pandas as pd
from multiprocessing import Pool
import functools
from os import cpu_count

def attachpandas():
    pd.core.frame.DataFrame.apply_parallel = df_apply_parallel

def df_apply_parallel(self, func, *static_data, num_processes=cpu_count(), **kwargs):
    """
    Add functionality to pandas so that you can do processing on dataframes on multiple cores at same time.
    - Set number of cores in num_processes. By default, uses the maximum available cores on your CPU.
    - Parameters of func() has to be passed and received as position arguments or keyword arguments.
    - This method will pass individual rows from dataframe to the func.

    Return
        Result as Series that can be stored in new column.
    """

    func = functools.partial(func, *static_data, **kwargs)
    with Pool(num_processes) as p:
        ret_list = p.map(func, [row for _, row in self.iterrows()])

    return pd.Series(ret_list, index=self.index)

pd.core.frame.DataFrame.apply_parallel = df_apply_parallel
