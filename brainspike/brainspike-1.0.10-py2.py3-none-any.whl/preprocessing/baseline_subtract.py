"""
baseline_subtract.py

Module to subtract baseline. 

"""

import numpy as np

from ..abf.abf_obj import ABF
from ..preprocessing.preprocessing_tools import find_startbaseline
from .preprocessing_utils import _find_sweep_data

###################################################################################################
###################################################################################################

def baseline_subtract(data, mode = None, baseline_segment = [0, 10]): 
    """
    Returns basic baseline substract as first-pass. 
    
    Subtracts each time series point from mean, median
    or baseline (calculated as mean across baseline_segment) values. 
    
    Sets to processed_sweepdata attr in data object along with paramaters. 
    
    Arguments
    ---------
    data (list of objects):
        list of data objects processed using loader.py.
        
    mode (str): 
        baseline subtracte mode type (median, mean, baseline).
        
    baseline_segment (list): 
        baseline segment selection (sec.) for baseline calculation
        with 'baseline' mode. 
    
    """
    
    if type is not None: 
        
        if isinstance(data, list): 
            for obj in data: 
                
                sweepdata, srate = _find_sweep_data(obj)
                
                try:
                    obj.preprocessed_params['baseline_subtract'] 
                    obj.preprocessed_params.update({'baseline_subtract': obj.preprocessed_params['baseline_subtract']\
                        + " + " + mode}) # if params exist + existing
                    
                except:
                    obj.preprocessed_params.update({'baseline_subtract': mode}) # set attr params 
                    
                # baseline subtraction
                #---------------------
                # note: to only be conducted in 
                # recordings from voltage clamp 
                # hence, no multidimensional arrays
                
                if len(sweepdata) == 1: 
            
                    if mode == 'baseline': 
                        baseline = find_startbaseline(sweepdata, srate, baseline_segment = baseline_segment)
                        obj.baselinecorr_sweepdata = sweepdata - (baseline)
                        obj.preprocessed_times = np.arange(0, len(obj.baselinecorr_sweepdata),1)/srate

                    elif mode == 'mean': 
                        obj.baselinecorr_sweepdata = sweepdata - (sweepdata.mean())
                        obj.preprocessed_times = np.arange(0, len(obj.baselinecorr_sweepdata),1)/srate
                        
                    elif mode == 'median': 
                        obj.baselinecorr_sweepdata = sweepdata - (np.median(sweepdata))
                        obj.preprocessed_times = np.arange(0, len(obj.baselinecorr_sweepdata),1)/srate
                        
                    else: 
                        raise KeyError(f"baseline subtract mode not found | select 1 of either: 'mean', 'median', 'baseline' ...")
                    
                else: 
                    raise ValueError(
                                    "voltage clamp recordings to only be used"
                                     f"for baseline subtraction | {len(sweepdata)} sweepdata found ..."
                                     )
            return data
        
        else:
            raise TypeError("no data object found ...")
        

