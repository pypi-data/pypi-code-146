"""
signal_drop.py

Modules to remove timeseries of signals < threshold. 

"""

import numpy as np 

from ..abf.abf_obj import ABF

from ..preprocessing.preprocessing_tools import find_startbaseline
from ..preprocessing.downsample import decimate

###################################################################################################
###################################################################################################

def exclude_signaldrop(data, abs_thresh = None, baseline_thresh_multiplier = None,\
                             std_thresh = None, baseline_segment = [0, 10], time_thresh = 2): 
    """
    Find idx of the absolute downsampled signal >= threshold and re-adjust data objects. 
    
    NOTE: by default; cut-off idx is included only if the downsampled signal (default, 5 Hz)
    surpasses the threshold for >= 2 seconds. 
    
    Arguments
    ---------
    data (list of objects):
        list of data objects processed using loader.py.
        
    abs_thresh (float): 
        threshold values for signal drop-off calculation. If non-abs values passed, will be converted to an abs value. 
    
    baseline_thresh_multiplier (float): 
        threshold value calculated as baseline * baseline_thresh_multipler
        
    std_thresh (float): 
        threshold value calculated as std_thresh * std of the downsampled signal 
        
    baseline_segment (list): 
        time interval for baseline calculation
        
    time_thresh (int): 
        time that signal >= threshold before exclusion.
        this is to account for signals that will drop-below a threshold
        and return to baseline. 
        
    """

    if isinstance(data, list): 

        for obj in data: 

            if isinstance(obj, ABF):
                
                try: 
                    sweepdata = obj.baselinecorr_sweepdata
                except AttributeError: 
                    raise AttributeError("do not conduct signal drop exclusion without a baseline subtraction ...")
                        
                try: 
                    obj.preprocessed_params
                except AttributeError: 
                    obj.preprocessed_params = ({})

                try: 
                    srate = obj.metadata['sample_rate_hz']
                except AttributeError:
                    print('no sampling rate found | re-load data with loader ...')

                # note: to only be conducted in 
                # recordings from voltage clamp 
                # hence, no multidimensional arrays
                #----------------------------------
                
                if len(sweepdata) == 1: 
                    
                    # downsample to 1 hz for baseline thresh calc
                    # (note: this can be changed to improve accuracy)
                    #-------------------------------------------------
                    
                    ds_signal = decimate(sweepdata[0], q = int(srate/5)) 
                    ds_times = np.arange(0, len(ds_signal), 1)/5

                    # check signal drop at threshold cutoffs
                    #----------------------------------------
                    
                    if abs_thresh is not None: 
                        exc_idx = np.where(abs(ds_signal) >= abs(abs_thresh)) # abs sweepdata

                        if len(exc_idx[0]) >= 5 * time_thresh:  
                            time_cutoff = ds_times[exc_idx[0][0]] # w/ ds_signal
                            obj.baselinecorr_sweepdata_dropped = [sweepdata[0][0:int(time_cutoff*srate)]]
                            obj.preprocessed_params.update({'signal_drop_time': time_cutoff, 'signal_drop_thresh': (abs_thresh)}) # set attr params 
                        else: 
                            obj.baselinecorr_sweepdata_dropped = np.nan
                            obj.preprocessed_params.update({'signal_drop_time': np.nan, 'signal_drop_thresh': (abs_thresh)}) 

                    elif baseline_thresh_multiplier is not None: 
                        baseline = find_startbaseline(sweepdata[0], srate, baseline_segment = baseline_segment)
                        exc_idx = np.where(abs(ds_signal) >= abs(baseline * baseline_thresh_multiplier)) # abs  
                        
                        if len(exc_idx[0]) >= 5 * time_thresh: 
                            time_cutoff = ds_times[exc_idx[0][0]] # w/ ds_signal
                            obj.baselinecorr_sweepdata_dropped = [sweepdata[0][0:int(time_cutoff*srate)]]
                            obj.preprocessed_params.update({'signal_drop_time': time_cutoff, 'signal_drop_thresh': (baseline * baseline_thresh_multiplier)}) 
                        else: 
                            obj.baselinecorr_sweepdata_dropped = np.nan
                            obj.preprocessed_params.update({'signal_drop_time': np.nan, 'signal_drop_thresh': (abs_thresh)}) 
                        
                    elif std_thresh is not None: 
                        exc_idx = np.where(abs(ds_signal) <= abs(ds_signal.std()) * std_thresh) # std calc. on ds voltage

                        if len(exc_idx[0]) >= 5 * time_thresh:
                            time_cutoff = ds_times[exc_idx[0][0]] # w/ ds_signal
                            obj.baselinecorr_sweepdata_dropped = [sweepdata[0][0:int(time_cutoff*srate)]]
                            obj.preprocessed_params.update({'signal_drop_time': time_cutoff, 'signal_drop_thresh': (ds_signal.std()) * std_thresh}) 
                        else: 
                            obj.baselinecorr_sweepdata_dropped = np.nan
                            obj.preprocessed_params.update({'signal_drop_time': np.nan, 'signal_drop_thresh': (abs_thresh)}) 
                            
                    else: 
                        raise ValueError("pass a threshold value ...")
                        
                else: 
                    raise ValueError("voltage clamp recordings to only be used"
                                    f"for baseline subtraction | {len(sweepdata)} sweepdata found ...")
                       
            else:
                raise TypeError("no data object found ...")
            
        return data 
                
    else:
        raise TypeError("no data object found")
    
    
