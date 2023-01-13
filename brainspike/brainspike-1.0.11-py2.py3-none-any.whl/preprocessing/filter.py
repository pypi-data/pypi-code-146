"""
filter.py

Modules for filtering intracellular voltage arrays. 

"""

from scipy import signal

import numpy as np

from ..abf.abf_obj import ABF

from .preprocessing_utils import _find_sweep_data

###################################################################################################
###################################################################################################

def low_pass(data, filter_order = 4, lowpass_cutoff = 10000):
    """
    Returns the low-pass sweepdata array with a butterworth filter
    from passed data object.  
    
    Sets to processed_sweepdata attr in data object along with paramaters. 
    
    Arguments
    ---------
    data (list of objects):
        list of data objects processed using loader.py.
        
    filter_order (int): 
        butterworth filter order.

    lowpass_cutoff (float):
        the cutoff frequency (in sample units, remember to divide it
        by the Nyquist frequency in sampling points).
    
    """
    
    print('applying low-pass Butterworth filter | '
          f'filter order: {filter_order}, lowpass_cutoff: {lowpass_cutoff} ...')
        
    if isinstance(data, list): 
        for obj in data: 
            
            sweepdata, srate = _find_sweep_data(obj)

            myparams = dict(btype='lowpass', analog=False)

            # generate filter kernel (a and b)
            if filter_order == None: 
                filter_order = 4 # default to 4th order if == None
                
            # apply filter to sweep data
            #----------------------------
            b, a = signal.butter(N = filter_order, Wn = lowpass_cutoff, **myparams, fs = srate)
            
            obj.preprocessed_params.update({'lowpass_filter_order': filter_order, 'lowpass_cutoff': lowpass_cutoff}) # set attr params 
            obj.preprocessed_sweepdata = signal.filtfilt(b,a, sweepdata) # set attr low passed sweepdata
            obj.preprocessed_times = np.arange(0, len(obj.preprocessed_sweepdata),1)/srate # adj times

        return data
    
    else:
        raise TypeError("no data object found")


def bessel_filter(data, filter_order = 1, lowpass_cutoff = 10000):
    """
    
    Returns the bessel filtered sweepdata array from a passed data object.
    Default to 1st orderm 10 KHz cut off. 
    
    Sets to processed_sweepdata attr in data object along with paramaters. 
    
    NOTE: use at your own cauti
    
    Arguments
    ---------
    data (list of objects):
        list of data objects processed using loader.py.
        
    filter_order (int): 
        butterworth filter order.

    lowpass_cutoff (float):
        the cutoff frequency (in sample units, remember to divide it
        by the Nyquist frequency in sampling points).

    """

    print('applying low-pass Bessel filter | '
          f'filter order: {filter_order}, lowpass_cutoff: {lowpass_cutoff} ...')
    
    if isinstance(data, list): 
        for obj in data: 
            
            sweepdata, srate = _find_sweep_data(obj)

            # default to 1st order if == None
            #--------------------------------
            if filter_order == None: 
                filter_order = 1    
                
            # check filter coef
            #------------------
            filt_coeff = (lowpass_cutoff) / (srate/ 2.)
            if filt_coeff < 0 or filt_coeff >= 1:
                raise ValueError("bessel coeff ({:f}) is outside of valid range [0,1]; cannot filter"
                                 "sampling frequency {:.1f} kHz with cutoff frequency {:.1f} kHz.".format(filt_coeff, srate, lowpass_cutoff))            

            # apply filter to sweep data
            #----------------------------
            myparams = dict(analog = False, norm = 'phase')

            b, a = signal.bessel(filter_order, lowpass_cutoff, 'low', **myparams, fs = srate) 

            obj.preprocessed_params.update({'bessel_filter_order': filter_order, 'bessel_cutoff': lowpass_cutoff}) # set attr params 
            obj.preprocessed_sweepdata = signal.filtfilt(b, a, sweepdata) 
            obj.preprocessed_times = np.arange(0, len(obj.preprocessed_sweepdata),1)/srate # adj times 
            
        return data
    
    else:
        raise TypeError("no data object found")
