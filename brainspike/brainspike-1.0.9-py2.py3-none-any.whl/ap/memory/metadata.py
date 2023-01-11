"""
memory_ap_metadata.py

Very basic metadata generation for in memory data. 
Simplified output for further processing. 
"""

# pandas 
import pandas as pd

# data extraction
from brainspike.ap.memory.data import MemoryApData

# error raise
class NoMetadataSelection(Exception): pass
class CheckType(Exception): pass

#---------------------

# numpy
import numpy as np

class MemoryApMetadata: 

    def __init__(self, current_steps, metadata, metadata_out = 'yes'): 
        """


        Arguments
        ---------


        Returns
        -------
        

        """

        # check metadata 'yes' or 'no'
        if metadata_out != 'yes' and metadata_out != 'no': 
            raise NoMetadataSelection(f"Metadata selection is either 'yes' or 'no' | currently set as {metadata_out}")

        # to maintain the flexibility of the API
        # users have the option to input their own metadata 
        # for ap_object outputs 
        if metadata_out == 'yes': 
            if isinstance(metadata, pd.DataFrame): 
                metadata['current_step_pa'] = [np.diff(current_steps)[0]]
                metadata['max_current_injected_pa'] = current_steps[-1]
                metadata['min_current_injected_pa'] = current_steps[0]
                metadata['sweep_count'] = len(current_steps)
            else: 
                raise CheckType("Metadata type | dict or DataFrame")

            self.metadata_df = metadata
        
        #-------------------
        # if 'no' metadata simplify out to identifier
        if metadata_out == 'no': 
            print(f'metadata_out: {metadata_out} | metadata will output the index of the input only')

            if isinstance(metadata, dict): 
                metadata = pd.DataFrame(metadata)

            self.metadata_df = pd.DataFrame({'idenfifier': metadata.index.values}) 