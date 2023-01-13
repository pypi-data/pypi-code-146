"""
preprocessing_tools.py

Tools for preprocessing modules (e.g. thresholds, baseline)

"""

import numpy as np 

###################################################################################################
###################################################################################################

def find_startbaseline(sweepdata, srate, baseline_segment = [0, 10]): 
    """
    Returns mean baseline value within baseline segment time window. 
    
    Arguments
    ---------
    
    sweepdata (arr): 
        arr of sweepdata
        
    srate (float, int): 
        sampling rate
        
    baseline_segment (list): 
        time interval for baseline calculation
    
    """

    baseline = np.mean(sweepdata[baseline_segment[0]*srate:baseline_segment[1]*srate]) # find baseline amplitude across time segment
    
    # print(f'baseline value of: {baseline} pA across {baseline_segment} seconds ...')

    return baseline


def rms(sweepdata, segment):
    """
    Calculates the square root of the mean square (RMS)
    along the segment.
    
    Arguments
    ---------
    data (array):
        numpy array with the data (e.g., voltage in microVolts)
        
    segment (int):
        The size of the segment to calculate (in sampling points)
        
    """

    a2 = np.power(sweepdata,2)
    kernel = np.ones(segment)/float(segment)

    return np.sqrt(np.convolve(a2, kernel, 'same') )


def find_thresh(sweepdata = None, srate = None, **threshold_parameters_kwargs): 
    """
    Find thresholds for PSC detections. 
    
    Arguments
    ---------
    sweepdata (arr): 
        sweepdata array. 

    srate (int): 
        sampling rate.
        
    threshold_parameters_kwargs (kwargs): 
        parameters for threshold detection. 
        threshold detect can be one of either:  'donoho', 'rms' or 'mean'. 
        donoho --> std estimated using donohos rule (https://www.nature.com/articles/s41598-021-93088-w)
        rms --> std above the rms, calculated within a time segment (rms_win_len). 
        outlier_removal --> similar to rms method, but std calculated on signal with outlier events removed > 10 std. 
        
    Returns
    -------
    Returns a list of low and high cut-off to be used for sweepdata detections, per channel.  
    
    """   

    # donohos rule
    #---------------
    # calculate std using donoho's rule
    # mutiply resulting std by upper and lower threshold limits
    
    if threshold_parameters_kwargs['thresh_detect_mode'] == 'donoho': 

        thr_low = np.median(abs(sweepdata)/0.6745)*threshold_parameters_kwargs['std_thresh'][0]
        thr_high = np.median(abs(sweepdata)/0.6745)*threshold_parameters_kwargs['std_thresh'][1]
        
    # absolute
    #----------
    # set absolute threshold 
    
    elif threshold_parameters_kwargs['thresh_detect_mode'] == 'abs': 

        thr_low = threshold_parameters_kwargs['abs_thresh'][0]
        thr_high = threshold_parameters_kwargs['abs_thresh'][1]

    # rms 
    #------------
    # find rms within selected window using sweepdata signal
    # median of sweepdata sweepdatalitude per channel
    # + rms * upper and lower thresholds
    
    elif threshold_parameters_kwargs['thresh_detect_mode'] == 'rms':
        
        myrms = rms(sweepdata, segment = int(threshold_parameters_kwargs['rms_win_len']*srate))

        thr_low = np.median(abs(sweepdata)) + myrms.std()*threshold_parameters_kwargs['std_thresh'][0]
        thr_high = np.median(abs(sweepdata)) + myrms.std()*threshold_parameters_kwargs['std_thresh'][1]

    # baseline
    #----------
    # find threshold values as a multiplier from 
    # baseline calculated within a time segment on the absolute sweepdata signal 
    
    elif threshold_parameters_kwargs['thresh_detect_mode'] == 'baseline':

        baseline = find_startbaseline(abs(sweepdata), srate, baseline_segment = threshold_parameters_kwargs['baseline_segment'])
        
        thr_low = baseline*threshold_parameters_kwargs['baseline_thresh_multiplier'][0]
        thr_high = baseline*threshold_parameters_kwargs['baseline_thresh_multiplier'][1]

    else: 
        raise AttributeError("no threshold parameters found")

    return thr_low, thr_high