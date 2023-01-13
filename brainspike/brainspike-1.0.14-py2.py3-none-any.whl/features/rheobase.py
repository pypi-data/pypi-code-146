"""
rheobase.py

Modules to find rheobase 
for sweep level spike analysis. 

"""

import numpy as np 
from numpy.lib.stride_tricks import sliding_window_view as window

import pandas as pd 

###################################################################################################
###################################################################################################

def return_rheobase(df_spiketrain, df_spikes): 
    """ returns rheobase (pA) from sweep train feature extractions (all sweeps) """

    avg_rate = df_spiketrain['avg_rate'].values
    sweep_numbers = np.unique(df_spiketrain['sweep_number'].values)
    
    # find where avg rate > 1 diff for consecutive sweeps 
    # this is to prevent a 'false' rheobase detection 
    avg_rate_diff = np.diff(avg_rate) 
    
    rheobase_idx = window(np.argwhere(avg_rate_diff >= 1), (2, 1))[np.diff(window(np.argwhere(avg_rate_diff >= 1),\
                (2, 1)), axis=2).ravel() == 1, :, :][0][0][0][0] # find idx w/in window 
    
    if avg_rate[rheobase_idx] == 0:
        
        rheobase_df = df_spiketrain[df_spiketrain['sweep_number'] == sweep_numbers[rheobase_idx+1]]
        rheobase = rheobase_df.stimulus.values[0]
        rheobase_sweepnumber = rheobase_df.sweep_number.values[0]
        
        return rheobase, rheobase_sweepnumber
    else: 
        return 0, 0 # no rheobase :: firing @ baseline
    