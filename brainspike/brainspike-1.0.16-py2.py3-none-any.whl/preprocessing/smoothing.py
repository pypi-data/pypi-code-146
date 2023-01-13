"""
smoothing.py

Modules for smoothing voltage arrays.

"""

import numpy as np

from ..abf.abf_obj import ABF

from .preprocessing_utils import _find_sweep_data

###################################################################################################
###################################################################################################

def convolution(data, win_len = 0.002): 
    """
    Returns a smoothed voltage array using a linear convolution. 
    
    Sets to processed_sweepdata attr in data object along with paramaters. 

    Arguments
    ---------
    data (list of objects):
        list of data objects processed using loader.py.
    
    win_len (float, default 0.002 s; 2 ms): 
        window length (seconds) for kernel size. 
        
    NOTE
    -----
    mode == 'valid': 
        returns output of length max(M, N).
        boundary effects are cropped.  
        https://numpy.org/doc/stable/reference/generated/numpy.convolve.html
        https://stackoverflow.com/questions/10006084/how-to-remove-the-boundary-effects-arising-due-to-zero-padding-in-scipy-numpy-ff
    
    """
    
    if isinstance(data, list): 
        for obj in data: 
            
            # collect sweepdata
            #-------------------
            # collect preprocessed sweepdata
            # if exists; default to sweep data
            
            sweepdata, srate = _find_sweep_data(obj)
                    
            # smooth each sweepdata
            #-----------------------
            # linear convolution (not multi-dimensional)
            
            smoothed = []; times = []
            for sweepnum in range(len(sweepdata)): 
                
                smoothed.append(np.convolve(sweepdata[sweepnum], np.ones(int(srate*win_len)),'valid') / (srate*win_len)) # linear convolution
                times.append(np.arange(0, len(obj.preprocessed_sweepdata[sweepnum]),1)/srate) # adj times for edge errs

            obj.preprocessed_sweepdata = smoothed # replace instance 
            obj.preprocessed_times = times
            
            # add parameters 
            #----------------
            try:
                obj.preprocessed_params['smoothing_window'] 
                obj.preprocessed_params.update({'smoothing_window': win_len +\
                    obj.preprocessed_params['smoothing_window']}) # if params exist + existing
                
            except:
                obj.preprocessed_params.update({'smoothing_window': win_len}) # set attr params 
                
            else:
                raise TypeError("no data object found ...")
            
        return data
