"""
spike_sweep_search.py 

Modules to find spike features
on selected sweep

"""

import pandas as pd 

import numpy as np 

###################################################################################################
###################################################################################################

def find_closestcurrentsweep(df_spiketrain, df_spikes, i_search = None): 
    """ return sweep feature df and spike firing sweep for closest current step """
    
    currentsteps = np.unique(df_spikes['peak_i'].values) # find unique current steps 

    diff = np.absolute(currentsteps - (i_search)) # find current step idx to i_search 
    closest_currentstep_idx = np.absolute(diff - 0).argmin() # account for negative vals
    
    df_spiketrain = df_spiketrain[df_spiketrain.stimulus == currentsteps[closest_currentstep_idx]] # isolate df spiketrain
    
    return df_spiketrain, df_spiketrain.sweep_number.values[0]


def find_maxfiringsweep(df_spiketrain, df_spikes): 
    """ return max firing sweep feature df and max firing sweep """
    
    avg_rate = df_spiketrain['avg_rate'].values
    
    max_avg_rate_idx = np.argmax(avg_rate)
    
    if max_avg_rate_idx.size == 1: 
        df_spiketrain = df_spiketrain[df_spiketrain.avg_rate == avg_rate[max_avg_rate_idx]]
        
        if len(df_spiketrain) > 1: # if > 1 max firing sweeps :: find sweep with highest peak v
            
            df_spikes = df_spikes[df_spikes['sweep_number'].isin(df_spiketrain['sweep_number'])] # spikes from corresponding sweeps 

            df_maxfiring_maxpeak = df_spikes[df_spikes.peak_v == max(df_spikes.peak_v)] # isolate sweep with max peak v 
            max_avg_rate_sweepnumber = (df_maxfiring_maxpeak.sweep_number.values[0])

            return df_spiketrain[df_spiketrain.sweep_number == max_avg_rate_sweepnumber], max_avg_rate_sweepnumber
        
        else: 
            return df_spiketrain, df_spiketrain['sweep_number'].values[0]
        
    else: 
        return df_spiketrain, None # not found 
    
    
def find_maxampspikes(df_spikes, sweep): 
    """ return spike feature df filterd for peak amplitudes """
    
    df_spikes = df_spikes[df_spikes.sweep_number == sweep]

    # find max peak_v spike for sweep 
    if len(df_spikes) > 1: 
        peak_v_idx = np.argmax(df_spikes.peak_v.values) 
        return df_spikes[df_spikes.peak_v == df_spikes.peak_v.values[peak_v_idx]]
    else: 
        return df_spikes
        
        