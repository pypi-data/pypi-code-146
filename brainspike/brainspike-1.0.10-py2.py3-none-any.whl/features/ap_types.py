"""
ap_types.py

Modules to determine 
ap types for iPSC neurons [https://www.nature.com/articles/mp2016158] 

"""

import math 

import numpy as np 

###################################################################################################
###################################################################################################

# to update this quantification ... 
# make a module for calculating 'aborted' spikes ... 

def return_aptype(df_spiketrain, min_peak, dv_cutoff, start, end): 
    """
    Breakdown the number of AP analysed into different AP types as cited [https://www.nature.com/articles/mp2016158]. 
    
    Calculated for default settings (min height >= 0 mV, dv/dt == 5). 
    Assumed to be calculated from max firing sweep. 

    Note: that ap type classification was based on 500 ms depolarisation steps, hence Hz metrics need to be considered.
    However, classification will stand for 1s + stimulations. 

    AP Type breakdown
    -----------------
    Type 5: >= 10 Hz firing freq
    Type 4: > 4  and < 10 Hz firing freq
    Type 2/3: > 0 and <= 2 avg_rate
    Type 1: == 0 Hz firing_freq
    
    Arguments
    ---------
    df_spiketrain (df): 
        df of all spike train features
    
    min_peak (float): 
        min peak for spike feature extraction 
        
    dv_cutoff (float):
        dv cutoff for spike detection 
        
    start, end (float): 
        stimuli start and end types

    Returns
    -------
    ap_type (int): classification ap type 1-5. 

    """
    
    end = round(end,1) # round nearest decimal
    start = round(start,1) 
    
    if (end-start >= 0.5) & (end-start <= 1): 

        if min_peak == 0 and dv_cutoff == 5: 

            if len(df_spiketrain) > 0:
                
                avg_rate = df_spiketrain.avg_rate.values
                
                if math.isnan(avg_rate) == False: 
                    
                    if avg_rate >= 10: 
                        ap_type = 'Type 5'
                    elif (avg_rate >= 2) and (avg_rate < 10): # can have aborted spikes 
                        ap_type = 'Type 4'
                    elif (avg_rate > 0) and (avg_rate < 2): # followed by aborted or no + spikes
                        ap_type = 'Type 2/3'
                    elif avg_rate == 0: 
                        ap_type = 'Type 1'
                    return ap_type
                
                else: 
                    return np.nan 
            else: 
                return np.nan
        else: 
            return 'min_peak != 0 & dv_cutoff != 5' # err msg 
    else: 
        return 'stim length not >= 0.5 & <= 1 seconds' # err msg 
    
