"""
psc_extractor.py

Modules for extracting psc event start + end times. 

"""

from scipy import signal

import numpy as np

###################################################################################################
###################################################################################################

# place the artefacts into here?? seeme like it should be part of the extractor ... 

def detect_putative_pscs(current, highthr = 5, distance = 0.002, srate = 50_000): 
    """ initial detection for psc event peaks"""

    peaks, _ = signal.find_peaks(x = abs(current), height = highthr, prominence = 1) 

    dx = np.diff(peaks)
    peaks_idx = np.where(dx>=distance*srate)[0] 

    return peaks_idx, peaks


def refine_psc_times(current, win_search_time = [0.05, 0.05], lowthr = None, peaks_idx = None, peaks = None, srate = 50_000): 
    """ refine psc event times - find start and end times """

    # +1 is the next peak after big time difference
    # add peak 0 because we count first start is the first detected peak
    start = np.concatenate( ([0], peaks_idx + 1) )
    try:
        pstart = peaks[start] # selection from all peaks 
    except IndexError:
        
        # if index 0 no peak detected
        pstart = np.nan
    else:
        
        for i, x in enumerate(pstart):
            
            # read backward w/in window time
            tmp = abs(current)[x-int(win_search_time[0]*srate):x]  

            # values below lower threshold
            val, = np.where( tmp < lowthr )

            try:
                pstart[i] -= (int(win_search_time[0]*srate)-val[-1]) 
                
            except IndexError:
                pass # do not assign new value if not found

    # the value after the big difference is the last 
    # add last peak detected as the end of a peak
    end = np.concatenate( (peaks_idx, [-1]) )
    
    # selection from all peaks
    try:
        pend = peaks[end]
    except IndexError:
        # if index 0 no peak detected
        pend = np.nan
    else:

        for i, x in enumerate(pend):
            
            # read forward w/in window time
            tmp = abs(current)[x+int(win_search_time[1]*srate):x:-1] 
            val, = np.where( tmp<lowthr ) 
            
            try:
                # because we look from outside we need to subtract
                pend[i] += (int(win_search_time[1]*srate)-val[-1]) 
            except IndexError:
                pass # do not assign value if not found

    return np.column_stack((pstart, pend))
