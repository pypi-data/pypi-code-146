"""
data.py

Class to load data from abf files. 

"""

import pyabf
import functools 

###################################################################################################
###################################################################################################

class ABFData: 

    def __init__(self, file_path, protocol = None): 
        """
        Data class for extraction of voltage and timearrays from the 
        *.abf file format across all sweeps. 
        
        Arguments
        ---------
        file_path (str): 
            abs path to *.abf file. 

        """
        
        self.abf_obj = pyabf.ABF(file_path) # abf object
        self.file_path = file_path
        self.protocol = protocol

        if self.protocol in ['ap', 'psc', None]:
            pass
        else: 
            raise ValueError(
                             'set a protocol for loader | '
                             'one of either: ap, psc or None ...'
                             )
        
    def _extract(sweep): 
        def _extract_dec(func): 
            @functools.wraps(func)
            def _extract_wrap(*args, **kwargs): 
                abf_obj = func(*args, **kwargs)
                
                values = []
                for sweepnumber in abf_obj.sweepList:
                    abf_obj.setSweep(sweepnumber) 
                    values.append(getattr(abf_obj,sweep))
                    
                return values
            return _extract_wrap
        return _extract_dec
    
    @property
    @_extract('sweepY')
    def sweepdata(self): 
        return self.abf_obj # sweep data (voltage in CC, current in VC)
    
    @property
    @_extract('sweepX')
    def times(self): 
        return self.abf_obj
    
    @property
    @_extract('sweepC')
    def commandwaveform(self): # current steps in CC, no current in 
        return self.abf_obj

    
