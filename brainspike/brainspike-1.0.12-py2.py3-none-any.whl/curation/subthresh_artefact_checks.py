"""
subthresh_artefact_checks.py

Modules to remove falsely detected subthreshold values. 

"""

import math 
import numpy as np

###################################################################################################
###################################################################################################

def rem_sag_amps(sag_voltages_fromsteady = None, amp_cutoffs = [-5, -200]): 
    """ find idx of subthreshold sweeps not within amplitude cutoff thresholds """

    if len(sag_voltages_fromsteady) > 0: 
        
        idx_keep = np.where((np.array(sag_voltages_fromsteady) >= amp_cutoffs[1]) \
            & (np.array(sag_voltages_fromsteady) <= amp_cutoffs[0]))
        
        return idx_keep
    
    else: 
        return None