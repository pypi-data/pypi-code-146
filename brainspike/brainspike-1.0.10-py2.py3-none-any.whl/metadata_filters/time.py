"""
times.py 

Modules for filtering recordings 
times in metadata. 

"""

import numpy as np

import pandas as pd

from datetime import date

###################################################################################################
###################################################################################################

def times(time_range = None): 
    """ return a range of times for metadata filtering """
    
    if time_range is not None: 
        if isinstance(time_range, list): 
            if len(time_range) == 2: 
                times = pd.date_range(start = time_range[0], end = time_range[1], freq="s")
    
    else: 
        raise KeyError("no list of times passed ...")

    return times.strftime("%H:%M:%S")

