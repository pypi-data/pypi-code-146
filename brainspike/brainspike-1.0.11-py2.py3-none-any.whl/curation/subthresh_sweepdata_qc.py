"""
subthresh_sweepdata_qc.py

Modules for quality control 
on sweep data for subthresh sweep data. 

"""

import numpy as np

import scipy 

from ..postprocessing.current_steps import calc_current_steps

###################################################################################################
###################################################################################################

def drop_depolsweeps(sweepdata, sweeptimes, stimuli): 
    """ drop sweeps with +ve stimuli injections """
    
    current_steps = calc_current_steps(stimuli) # find current steps 
    hyperpol_current_idx = np.where(np.array(current_steps) <= 0) # idx of hyperpol + 0 pA stimuli sweeps 
    adjusted_sweepnumbers = hyperpol_current_idx[0]
    
    if len(hyperpol_current_idx[0]) > 1: # adjust v, t, i

        sweepdata = np.array(sweepdata)[hyperpol_current_idx]
        sweeptimes = np.array(sweeptimes)[hyperpol_current_idx]
        stimuli = np.array(stimuli)[hyperpol_current_idx]
        
    else: 
        pass 
    
    return sweepdata, sweeptimes, stimuli, adjusted_sweepnumbers
        

def drop_unstablesweeps_rms(sweepdata, sweeptimes, stimuli, end = None, srate = None, rms_cutoff = 0.2, baseline_interval = 0.03): 
    """ drop unstable sweeps outside rms cutoffs on end - baseline_intreval segment only """
    
    # find idx of unstable sweeps
    #----------------------------
    sweep2keep, _ = _measure_subthresh_sweep_rmsinstability(sweepdata, rms_cutoff = rms_cutoff, end = end, srate = srate,\
                                                    baseline_interval = baseline_interval) 
    
    # dropped_count = ( len(sweepdata) - len(sweep2keep[0]) ) 
    # print(f'total of {dropped_count} sweeps dropped <= {rms_cutoff} rms cutoff ...')
    
    # drop unstable sweepdata
    #-------------------------
    sweepdata = np.array(sweepdata)[sweep2keep]
    
    # adjust times + stimuli
    #------------------------
    sweeptimes = np.array(sweeptimes)[sweep2keep]
    stimuli = np.array(stimuli)[sweep2keep]
    
    return sweep2keep, sweepdata, sweeptimes, stimuli


def measure_linregress(i = None, v = None): 
    """ measure linear regression for v x i values :: sanity check for ri calculations """
    
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(i, v)

    linregress_dict = {'slope': slope, 'intercept': intercept,\
                        'r2_value': r_value**2, 'p_value': p_value, 'std_err': std_err}
    
    return linregress_dict


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


def _measure_subthresh_sweep_voltageinstability(sweepdata, end = None, start = None, srate = None, baseline_interval = 0.1): 
    """ drop unstable sweeps with positive voltage differences betwen start and end intervals on hyperpol sweeps """
    
    if (srate is not None) and (end is not None) and (start is not None): 
        
        if len(sweepdata) < 1:
            return 0, 0
        
        mean_start_voltages = []; mean_steady_voltages = []
        for data in sweepdata: 
            start_v = data[int(start*srate):int(start*srate)+int(baseline_interval*srate)] # find baseline voltage
            steady_v = data[int(end*srate)-int(baseline_interval*srate):int(end*srate)] # find ss voltage

            start_mean = np.mean(start_v)
            steady_mean = np.mean(steady_v)

            mean_start_voltages.append(start_mean)
            mean_steady_voltages.append(steady_mean)
            
        return mean_start_voltages, mean_steady_voltages
    
    else: 
        raise ValueError(f'pass start, end and srate values | start: {start}, srate: {srate}, end: {end} ...')
