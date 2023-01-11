"""
psc_artefact_checks.py

Modules to remove falsely detected PSCs. 

"""

import numpy as np

from scipy import signal

import math 

###################################################################################################
###################################################################################################

def rem_overlap_events(event_times = None, overlap_time_thresh = 0, srate = 50_000): 
    """ remove overlapping PSC events """

    try: 
        pstart = event_times[:,0]
        pend = event_times[:,1]

        try: 
            overlap_times_start = np.diff(pstart)
            idx_start = np.where(overlap_times_start <= overlap_time_thresh*srate)
            pstart = np.delete(pstart, idx_start) 
            pend = np.delete(pend, idx_start)
        
        except ValueError: 
            pstart = []; pend = [] 
            
    except IndexError: 
        pstart = []; pend = [] 

    return np.column_stack((pstart, pend))


def merge_events(event_times = None, srate = 50_000, merge_time_thresh = 0.025): 
    """ merge PSCs """
    
    try: 
        pstart = event_times[:,0]
        pend = event_times[:,1]

        try: 

            # time diff between start - end times
            hfo_times_diff = []
            for diff in zip(pstart[1:], pend): # start 2nd - end 1st
                overlap_times = np.subtract(diff[0], diff[1])/srate
                hfo_times_diff.append(overlap_times)

            merge_idx = np.where(np.array(hfo_times_diff) <= merge_time_thresh) # idx to merge if < merge times
            pstart = np.delete(pstart, merge_idx[0]+1) 
            pend = np.delete(pend, merge_idx[0])# delete pend of event before merge_idx 
            
        except ValueError: 
            pstart = []; pend = [] 
            
    except IndexError: 
        pstart = []; pend = [] 

    return np.column_stack((pstart, pend))  


def rem_amps(sweepdata = None, event_times = None, amp_cutoffs = None): 
    """ remove events not within amplitude cutoff thresholds """

    try: 
        pstart = event_times[:,0]
        pend = event_times[:,1]

        try: 
            
            max_amp_pks = []
            for start, end in zip(pstart, pend):
                
                if (math.isnan(start) is False) & (math.isnan(end) is False): 
                    
                    max_amp = max(abs(sweepdata)[start:end])
                    max_amp_pks.append(max_amp)
                    
                else: 
                    pass

            inc_peaks = [n for n,i in enumerate(max_amp_pks) if ((i<= amp_cutoffs[1]) & ((i>= amp_cutoffs[0])))]  
    
            pstart = pstart[inc_peaks]
            pend = pend[inc_peaks] 
            
        except ValueError: 
            pstart = []; pend = [] 
            
    except IndexError: 
        pstart = []; pend = [] 

    return np.column_stack((pstart, pend))   


def rem_shortdur(event_times = None, srate = 50_000, duration_time_cutoffs = [0.001, 0.020]): 
    """ remove short duration events """
    
    try: 
        pstart = event_times[:,0]
        pend = event_times[:,1]
    
        try: 

            burst_dur = (pend-pstart)/srate 

            idx= np.where((burst_dur <= duration_time_cutoffs[0]) | (burst_dur >= duration_time_cutoffs[1])) # remove events outside 
            
            pstart = np.delete(pstart, idx) 
            pend = np.delete(pend, idx)
            
        except ValueError: 
            pstart = []; pend = [] 
            
    except IndexError: 
        pstart = []; pend = [] 

    return np.column_stack((pstart, pend))  


def rem_edge_events(sweepdata = None, event_times = None): 
    """ remove edge events """

    try: 
        pstart = event_times[:,0]
        pend = event_times[:,1]
        
        peak_start_idx = np.where(pstart <= 0)
        peak_end_idx = np.where(pend >= len(sweepdata)) 

        # start frame
        try: 
            peak_start_idx
            
            pstart = np.delete(pstart, peak_start_idx) # delete at same idx
            pend = np.delete(pend, peak_start_idx)
            
        except AttributeError: 
            pass
        
        # end frame
        try: 
            peak_end_idx
            
            pstart = np.delete(pstart, peak_end_idx) 
            pend = np.delete(pend, peak_end_idx)
            
        except AttributeError: 
            pass
            
    except IndexError: 
        pstart = []; pend = []    

    return np.column_stack((pstart, pend))  


def rem_opposite_polarity(sweepdata = None, baseline = None, event_times = None, polarity = None): 
    """ remove events with incorrect polarity relative to lowthr """


    if polarity is not None: 
        if (polarity == 'positive') | (polarity == 'negative'): 
            pass 
        else: 
            raise AttributeError(f"polarity must be 'positive' or 'negative'")
        
    else: 
        raise AttributeError(f"polarity not found | {polarity}")
    
    try: 
        pstart = event_times[:,0]
        pend = event_times[:,1]
        
        idx_remove = []
        for count, event_times in enumerate(zip(pstart, pend)): 
            
            sweepdata_filt = sweepdata[event_times[0]:event_times[1]] # sub-select sweepdata @ event times 
            
            if polarity == 'positive': # remove events < lowthr
                if max(sweepdata_filt) <= baseline: 
                    idx_remove.append(count)
                
            if polarity == 'negative':
                if max(sweepdata_filt) >= baseline: 
                    idx_remove.append(count)
                    
        pstart = np.delete(pstart, idx_remove)
        pend = np.delete(pend, idx_remove)

    except IndexError: 
        pstart = []; pend = []    
        
    return np.column_stack((pstart, pend))  




