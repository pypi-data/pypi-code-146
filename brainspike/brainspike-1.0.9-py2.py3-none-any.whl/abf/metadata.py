"""
metadata.py

Metadata extraction for patch-clamp acquired files. 

"""

import numpy as np

import pyabf

from ..postprocessing.current_steps import calc_current_steps
from ..postprocessing.stimulus_start_end import start_end_stimulus_times
from . data import ABFData

###################################################################################################
###################################################################################################

class ABFMetadata(ABFData): 

    def __init__(self, file_path, protocol = None): 
        """
        Metadata class for *.abf files. Returns
        dict with metadata required for further pre-
        and post-processing. 

        Arguments
        ---------
        file_path (str): 
            abs path to *.abf file. 

        """
        
        super().__init__(file_path, protocol = None)
        
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
        
    @property
    def metadata(self): 

        metadata_dict = dict(file_path = self.file_path,\
                             abf_id = self.abf_obj.abfID,\
                             date = self.abf_obj.abfDateTimeString[0:10],\
                             rec_time = self.abf_obj.abfDateTimeString[11:-4],\
                             sample_rate_hz = self.abf_obj.sampleRate,\
                             sweep_length_sec = self.abf_obj.sweepLengthSec,\
                             channel_count = self.abf_obj.channelCount,\
                             data_length_min = self.abf_obj.dataLengthMin,\
                             sweep_count = self.abf_obj.sweepCount,\
                             channel_list = self.abf_obj.channelList,\
                             file_comment = self.abf_obj.abfFileComment,\
                             tag_comment = self.abf_obj.tagComments,\
                             abf_version = self.abf_obj.abfVersionString) 
        
        if self.protocol == 'ap': 
            
            # add current steps 
            #------------------
            current_steps = calc_current_steps(self.commandwaveform)
            metadata_dict['current_step_pa'] = np.diff(current_steps)[0]
            metadata_dict['max_current_step_pa'] = current_steps[-1]
            metadata_dict['min_current_step_pa'] = current_steps[0]
            
            # add stimuli start + end times
            #------------------------------
            start, end = start_end_stimulus_times(self.commandwaveform)
            metadata_dict['start_sec'] = start/self.abf_obj.sampleRate
            metadata_dict['end_sec'] = end/self.abf_obj.sampleRate
            metadata_dict['start'] = start
            metadata_dict['end'] = end
            
        return metadata_dict
    
    
        
