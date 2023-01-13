"""
stimulus_start_end.py 

Modules for start and end 
times for stimulus. 

Note: these are assumed to be constant
across all sweepdata.

"""

import numpy as np

###################################################################################################
###################################################################################################

def start_end_stimulus_times(commandwaveform): 
    """
    Find start and end stimulus times from 
    command waveform array. 

    Arguments
    ---------
    commandwaveform (arr): 
        arr of depol/hyperpol steps used for stimulus 
        across all sweeps. 

    Returns
    -------
    start (float): start of stimulus interval in seconds
    end (float): end of stimulus interval in seconds
    
    """

    stimulus_idx = np.nonzero(commandwaveform)
    
    return stimulus_idx[1][0], stimulus_idx[1][-1]