"""
date.py 

Modules for filtering dates in 
metadata. 

"""

import numpy as np

import pandas as pd

from datetime import date

###################################################################################################
###################################################################################################

def dates(date_range = None): 
    """ return a range of dates for metadata filtering """

    if date_range is not None: 
        
        if isinstance(date_range, list): 
            
            if len(date_range) == 2: 
                
                for x in range(2): 
                    val = date_range[x].replace('-', ' ')
                    val = val.split(' ')
                    val = list(map(int, val)) 
                    
                    if x == 0: 
                        start_date = date(val[0], val[1], val[2]) # find dates 
                    if x == 1: 
                        end_date = date(val[0], val[1], val[2])
                        
                days = pd.date_range(start = start_date, end = end_date, freq='D') # create date range
                
            else: 
                raise KeyError("pass 2 dates ...")
            
        else: 
            raise KeyError("pass a list of 2 dates ...")
        
    else: 
        raise KeyError("no list of dates passed ...")

    return days.strftime('%Y-%m-%d').values

