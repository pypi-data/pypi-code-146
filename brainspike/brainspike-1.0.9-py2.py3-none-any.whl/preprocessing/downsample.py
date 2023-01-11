"""
downsample.py

Modules to decimate signal. 

"""

from scipy import signal

###################################################################################################
###################################################################################################

def decimate(sweepdata, q):
    """
    Down-sample the signal after applying an order 8
    Chebyshev type I FIR antialiasing filter. A Hamming window
    is used (see scipy.signal.decimate for details).
    
    Arguments
    ---------
    data : array_like
        The signal to be downsampled, as a N-dimensional array
        
    q : int
        The downsampling factor
    
    Returns:
    --------
    The down-sampled signal.
    """
    
    return signal.decimate(sweepdata, q, ftype = 'fir')