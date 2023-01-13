"""
ap_metadata.py

Michael Zabolocki, Aug 2022

Metadata extraction for patch-clamp acquired files. 
"""

# metadata filter 
import brainspike.ap.curation.metadata_filter as metadata_filter

# ap loader 
import brainspike.ap.loader as ap_loader

# libraries
import os
import numpy as np
import pandas as pd
from datetime import date, timedelta

# error raise
class NotAList(Exception): pass
class MultipleInputs(Exception): pass

#---------------------

def get_metadata(metadata): 
    """
    Get metadata. 

    Arguments
    ---------
    metadata (list or str):
        list of objects (processed ap_loader.py) or list of file_paths to 
        data file (e.g. *.abf)

    Returns
    -------
    Return dataframe of metadata, or ammended list of objects 
    for filtered parameters. 
    """

    metadata_all = []
    if isinstance(metadata, list):

        for x in range(len(metadata)): 
            if type(metadata[x]) != str: 
                metadata_all.append(metadata[x].metadata)

            elif type(metadata[x]) == str: 
                abf_file_paths = ap_loader.abf_filepath_check(ap_loader.find_all_filepaths(metadata)) # abf file paths
                metadata_all = metadata_concat(ap_loader.load(abf_file_paths)) 
                return pd.concat(metadata_all)

    if isinstance(metadata, str):
        abf_file_paths = ap_loader.abf_filepath_check(ap_loader.find_all_filepaths(metadata)) # abf file paths
        metadata_all = metadata_concat(ap_loader.load(abf_file_paths)) 

    return pd.concat(metadata_all)
    

def metadata_concat(data): 
    """
    Return concatenated metadata df out. 
    """

    metadata_all = []
    for x in range(len(data)): 
        metadata_all.append(data[x].metadata)

    return metadata_all


def get_objects_from_metadata(metadata): 
    """
    Returns object from metadata. 
    """
    
    data = []
    data_filepaths = []
    for m in metadata.index:
        data_filepaths.append(metadata.loc[m, 'file_path'])
       
    abf_file_paths = ap_loader.abf_filepath_check(ap_loader.find_all_filepaths(data_filepaths)) # abf file paths
    
    return ap_loader.load(abf_file_paths)
    









