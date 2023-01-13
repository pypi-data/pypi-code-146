"""
preprocessing_utils.py


collection of small modules which make
common preprocessing code  shorter. 

"""

import math 

import numpy as np

from ..abf.abf_obj import ABF

###################################################################################################
###################################################################################################

def _find_sweep_data(obj): 
    """ find preprocessed or unprocessed sweepdata from data object instances """
    
    if isinstance(obj, ABF):
        
        # search for preprocessed sweepdata
        #----------------------------------
        # if no preprocessed data, default to 
        # unpreprocessed data 
        
        try: 
            sweepdata = obj.baselinecorr_sweepdata_dropped
            
            try: 
                if math.isnan(sweepdata): 
                    sweepdata = obj.baselinecorr_sweepdata # default to preprocessed + baselinecorr
            except: 
                pass
            
        except AttributeError:
             
            try: 
                sweepdata = obj.baselinecorr_sweepdata
            except AttributeError: 
                
                try: 
                    sweepdata = obj.preprocessed_sweepdata 
                except: 
                    sweepdata = obj.sweepdata 
            
        # search for preprocessed params
        #--------------------------------
        # if none, create an instance
        
        try: 
            obj.preprocessed_params
        except: 
            obj.preprocessed_params = ({})

        # find sampling rate 
        #-------------------
        
        try: 
            srate = obj.metadata['sample_rate_hz']
        except AttributeError:
            print('no sampling rate found | re-load data with loader ...')
            
    else:
        raise TypeError("no data object found ...")
    
    return sweepdata, srate