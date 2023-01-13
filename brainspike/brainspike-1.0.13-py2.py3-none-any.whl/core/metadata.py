"""
metadata.py

Metadata extraction for patch-clamp acquired files. 

"""

import pandas as pd

from ..abf.metadata import ABFMetadata
from ..utils.paths.find_paths import file_extensionfilt

###################################################################################################
###################################################################################################

def metadata(file_path = None, protocol = None): 
    """
    Return metadata dict for *.abf files in file path. 
    
    Arguments
    ---------
    file_path (str, list or arr): 
        paths to action potential files. 
        note: *.abf files only accepted.  
    
    Raises
    ------
    TypeError: 
        no file path passed
        
    """

    metadata = []
    if file_path is not None: 
        
        file_path = file_extensionfilt(file_path, extension = '.abf') # check if dir + unpack

        for file in file_path: 

            metadata.append(ABFMetadata(file_path = file, protocol = protocol).metadata)

        return metadata
    
    else:
        raise TypeError(f"pass a path to file | {file_path}")






