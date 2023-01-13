"""
psc_categorization.py

Modules for categorizing PSCs
into event types (e.g. singlets, doublets ...)

"""

import numpy as np 

import pandas as pd 

from scipy import signal

###################################################################################################
###################################################################################################

# split this up into separate features .... psc_ .... psc_features ??? see what can be done here ... 

def event_categorisation(event_times = None, sweepdata = None, highthr = None, srate = 50_000): 
    """ PSC event categorization """

    event_category = []; peak_times_out = []; peak_amps_out = [];
    event_dur_out = []; postsyn_count = []; count_out = []
    
    for count, PSC_time in enumerate(event_times):  
        
        peaks, _ = signal.find_peaks(abs(sweepdata)[PSC_time[0]:PSC_time[1]], height = highthr, prominence = 1, distance = srate*0.002) 
        
        # re-adjust times
        peak_times = PSC_time[0] + peaks
        peak_times_out.append(peak_times)
        
        # amplitudes
        peak_amps = abs(sweepdata)[peak_times]
        peak_amps_out.append(peak_amps)
        
        # event duration
        event_dur = PSC_time[1] - PSC_time[0] # duration of event (not individual spikes)
        event_dur_out.append((event_dur/srate)*1000) # milisec conversion
        
        # event count
        count_out.append(count)

        # event categorisation 
        if len(peaks) > 0:
            if len(peaks) == 1: 
                event_category.append('singlet')
                postsyn_count.append(1)
                
            if len(peaks) == 2: 
                event_category.append('doublet')
                postsyn_count.append(2)
                
            if len(peaks) == 3: 
                event_category.append('triplet')
                postsyn_count.append(3)
                
            if len(peaks) >= 4: 
                event_category.append('burst')
                postsyn_count.append(4) 
                                                
        else: 
            event_category.append(np.nan)
            postsyn_count.append(np.nan)

    df_pscs = pd.DataFrame({'event_count': count_out, 'category': event_category, 'post_synaptic_count': postsyn_count,\
                            'event_start': event_times[:,0], 'event_end': event_times[:,1], 'peak_times': peak_times_out,\
                            'peak_amp': peak_amps_out, 'event_duration_ms': event_dur_out})
    
    df_pscs = df_pscs.set_index('event_count')

    return df_pscs
