"""
abf_ap_metadata.py

Michael Zabolocki, Aug 2022

Metadata extraction for patch-clamp acquired files. 
"""

# parent
from brainspike.ap.abf.data import AbfApData

# libraries
import pandas as pd
import pyabf
import numpy as np

# error raise
class NoMetadataSelection(Exception): pass

#---------------------

class AbfApMetadata(AbfApData): 

    def __init__(self, file_selected, current_steps, lowpass_cutoff, filter_order, win_len, metadata_out = 'yes'): 
        """
        

        Arguments
        ---------


        Returns
        -------
        

        """

        super().__init__(file_selected, lowpass_cutoff, filter_order, win_len)

        if metadata_out != True and metadata_out != False: 
            raise NoMetadataSelection(f"Metadata selection is a boolean | currently set as {metadata_out}")

        if metadata_out == True: 
            self.metadata_df = pd.DataFrame({'file_path': file_selected, 'abf_id': [self.abf.abfID], 'date': [self.abf.abfDateTimeString[0:10]],\
                'time_of_recording': [self.abf.abfDateTimeString[11:-4]], 'current_step_pa': [np.diff(current_steps)[0]],\
                            'max_current_injected_pa': current_steps[-1], 'min_current_injected_pa': current_steps[0],\
                                'sample_rate_hz': [self.abf.sampleRate],'sweep_length_sec': [self.abf.sweepLengthSec],\
                            'channel_count': [self.abf.channelCount], 'datalength_min': [self.abf.dataLengthMin], 'sweep_count': [self.abf.sweepCount],\
                                'channel_list': self.abf.channelList, 'file_comment': [self.abf.abfFileComment], 'tag_comment': self.abf.tagComments,\
                                    'abf_version': [self.abf.abfVersionString], 'pre_lowpass_cutoff': lowpass_cutoff, 'pre_filter_order': filter_order,\
                                        'pre_smoothing_window_sec': win_len}) 

            self.metadata_df.set_index('abf_id', inplace = True) # index as abf_id

        # simplify out to file_path and id for metadata_out == False 
        if metadata_out == False: 
            self.metadata_df = pd.DataFrame({'file_path': file_selected, 'abf_id': [self.abf.abfID], 'sample_rate_hz': [self.abf.sampleRate]}) 
            self.metadata_df.index = self.metadata_df['abf_id'] # index as abf_id