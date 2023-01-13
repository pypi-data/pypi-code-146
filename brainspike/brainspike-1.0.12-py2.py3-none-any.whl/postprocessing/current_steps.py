"""
current_steps.py 

Modules for finding current steps
from current arrays. 

"""

import numpy as np

###################################################################################################
###################################################################################################

def calc_current_steps(commandwaveform): 
    """
    
    Returns arr of command waveform injected per step (pA) 
    and the index of injection start. 
    
    Arguments
    ---------
    commandwaveform (arr): 
        arr of depol/hyperpol steps used for stimulus 
        across all sweeps. 

    Returns
    -------
    current_steps (arr): 
        current step per sweep
    
    current_start_end (arr): 
        idx of start of current step injection
    
    Raises
    ------
    CurrentCheck: 
        no current stimulus found

    """

    step_calc_max = np.amax(commandwaveform, axis=1) # max current injection (+ve polarity)
    step_calc_min = np.amin(commandwaveform, axis=1) # min current injection (-ve polarity) 
    current_steps = step_calc_max - abs(step_calc_min)  # current delta 

    return current_steps 


