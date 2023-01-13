"""
dataframes.py

Modules for exporter utilities. 

"""

import os
import json 

import numpy as np

import pandas as pd

from ..utils.plots.save import (create_path)

###################################################################################################
###################################################################################################


def export_df(data = None, df = None, fdir = None, fname = None, file_extension = '.xlsx'): 
    """ export df w/ metadata and preprocessing parameters attached """

    if df is not None: 
        
        # export 
        if None not in [fdir, fname, file_extension]:
            if file_extension == '.xlsx': 
                fname = create_path(fdir, fname, file_extension)
                print(f"saving df to {fname} ...")
                df.to_excel(fname)   
            else: 
                print(f'unable to export {file_extension} formats ...')
        else: 
            pass 
    else: 
        raise TypeError('pass df for exporting ...')
    


#----------------
## OLD
#----------------

#     # save file out 
#     if file_extension == '.xlsx': 
#         df.to_excel(fname)

#     elif file_extension == '.csv': 
#         df.to_csv(fname) 

#     elif file_extension == '.json': 
#         json_out_file = open(fname, "w") 
#         json.dump(df.reset_index().to_json(), json_out_file, indent = 6) 
#         json_out_file.close() 

#     # elif file_extension == '.txt': 
#     #     df.to_csv(filename, header=None, index=None, sep='\t', mode='a')

#         ## to re-import json as df
#         # f = open('analysed/test/report_summary_nometadata.json')
#         # data1 = json.load(f) # returns JSON object as a dictionary
#         # df = pd.read_json(data1) # converting it into dataframe

#     else: 
#         raise TypeError("save filename as either .xlsx, .csv, .json or .txt")
