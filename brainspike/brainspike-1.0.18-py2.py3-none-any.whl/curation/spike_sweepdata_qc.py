"""
spike_sweepdata_qc.py

Modules for quality control 
on sweep data for spike sweepdata. 

"""

import numpy as np

import scipy 

from ..postprocessing.current_steps import calc_current_steps

###################################################################################################
###################################################################################################

def drop_hyperpolsweeps(sweepdata, sweeptimes, stimuli): 
    """ drop sweeps with -ve stimuli injections """
    
    current_steps = calc_current_steps(stimuli) # find current steps 
    depol_current_idx = np.where(np.array(current_steps) >= 0) # idx of hyperpol + 0 pA stimuli sweeps 
    adjusted_sweepnumbers = depol_current_idx[0]
    
    if len(depol_current_idx[0]) > 1: # adjust v, t, i

        sweepdata = np.array(sweepdata)[depol_current_idx]
        sweeptimes = np.array(sweeptimes)[depol_current_idx]
        stimuli = np.array(stimuli)[depol_current_idx]
        
    return sweepdata, sweeptimes, stimuli, adjusted_sweepnumbers       

        
def drop_unstablesweeps_rms(sweepdata, sweeptimes, stimuli, end = None, srate = None, rms_cutoff = 0.2, baseline_interval = 0.03): 
    """ drop unstable sweeps outside rms cutoffs on end - baseline_intreval segment only """
    
    # find idx of unstable sweeps
    #----------------------------
    sweep2keep, _ = _measure_subthresh_sweep_rmsinstability(sweepdata, rms_cutoff = rms_cutoff, end = end, srate = srate,\
                                                    baseline_interval = baseline_interval) 
    
    # drop unstable sweepdata
    #-------------------------
    sweepdata = np.array(sweepdata)[sweep2keep]
    
    # adjust times + stimuli
    #------------------------
    sweeptimes = np.array(sweeptimes)[sweep2keep]
    stimuli = np.array(stimuli)[sweep2keep]
    
    return sweep2keep, sweepdata, sweeptimes, stimuli


def _measure_subthresh_sweep_rmsinstability(sweepdata, rms_cutoff = 0.2, end = None, srate = None, baseline_interval = 0.03):
    """ find trace instability for all sweepdata within baselineinterval"""
    
    if (srate is not None) and (end is not None): 
    
        if len(sweepdata) < 1:
            return 0, 0
        
        # find steady voltage
        #--------------------
        # calculate rms for all sweepdata
        # within baseline intervals 
        
        rms = []
        for data in sweepdata: 
            steady = data[int(end*srate)-int(baseline_interval*srate):int(end*srate)] # find steady state voltage
            mean = np.mean(steady)
            rms.append(np.sqrt(np.mean(np.square(steady-mean))))

        if rms_cutoff is not None: 
            sweep2keep = (np.where(np.array(rms) <= rms_cutoff)) # find sweeps <= rms_cutoff 
        else: 
            raise ValueError('no rms_cutoff set ...')
        
        return sweep2keep, rms
    
    else: 
        raise ValueError(f'pass end and srate values | srate: {srate}, end: {end} ...')