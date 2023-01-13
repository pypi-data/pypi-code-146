
""" 
spike_artefact_checks.py 

Modules for additional artefact checks / removals
from spike and/or spiketrain data. 

"""

import numpy as np 

import pandas as pd 

###################################################################################################
###################################################################################################

def rem_troughs(spikes_features, end_time): 
    """ delete artefactual troughs near end of current stimulus detected due to current drop-off """ 

    clip_time = 0.0002 # remove troughs < 0.2 ms from current stimulus end

    if "trough_t" in spikes_features.columns:
        troughs_clippingstim = spikes_features[(spikes_features['trough_t'] >= (end_time-clip_time))].index 
        if troughs_clippingstim.size > 0: 
            spikes_features.at[troughs_clippingstim[0],'trough_t'] = np.nan 

    return spikes_features