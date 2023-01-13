"""
ap_loader.py

Michael Zabolocki, Aug 2022

Main loader class for action potential files. 
"""

# libraries
import pyabf
import os
import numpy as np
import pandas as pd

# abf loader
import brainspike.ap.abf.loader as abf_ap_loader

# in memory loader
import brainspike.ap.memory.loader as memory_ap_loader

# error raise
class NoFilePathFound(Exception): pass
class NoAbfFilesFound(Exception): pass
class FilePathError(Exception): pass
class NoData(Exception): pass

#-----------------------------

def load(file_location_paths = None, times = None, stimuli = None, voltages = None, metadata = None, metadata_out = True,
lowpass_cutoff = None, filter_order = None, win_len = None): 
    """
    Load all files from a single file path
    or a directory. 

    Arguments
    ---------
    file_location_paths (list or str): 
        File paths can be parsed as a single
        string or a list of strings. 
        
    metadata_out (str): 
        --> change this to a boolean!?

    Returns
    -------
    ap_object (obj): 
        contains data and metadata. 
    """

    # add a filter and a convolution here for the raw files
    # --> add these all to the metadata also?? 

    #--------------------
    # process in memory loaded files and not file paths
    # place in key metadata 
    if (times is not None) and (stimuli is not None) and (voltages is not None)\
        and (metadata is not None) and (file_location_paths is None):

        ap_object = memory_ap_loader.load(times, stimuli, voltages, metadata, metadata_out)

    #--------------------
    # if not loaded files in memory
    # find file_paths and process in dataframe input
    if (times is None) and (stimuli is None) and (voltages is None) and (file_location_paths is not None):
        if isinstance(file_location_paths, pd.DataFrame): 
            file_location_paths = file_location_paths.file_path.values.tolist() # generated from metadata df out

        # find all file paths
        file_paths = find_all_filepaths(file_location_paths)

        # load files
        abf_file_paths = abf_filepath_check(file_paths) # select for abf files
        ap_object = abf_ap_loader.load(abf_file_paths, metadata_out, lowpass_cutoff, filter_order, win_len) # abf objects 

    return ap_object


###################
# file path checks
###################


def find_all_filepaths(file_location_paths): 
    """
    Find all file paths in directory.

    Arguments
    ---------
    
    """
    #-------------
    # load all files in path
    # if single string input
    if isinstance(file_location_paths, str): 

        file_paths = filepath_check(file_location_paths) # check file paths

        if len(file_paths) == 0: 
            raise NoFilePathFound("No file paths found") # raise error

    # if string list input
    if isinstance(file_location_paths, list): 
        
        file_paths = []
        for file_dir in file_location_paths: 
            file_paths.append(filepath_check(file_dir)) # check file paths

        if len(file_paths) == 0: 
            raise NoFilePathFound("No file paths found") # raise error
        else: 
            file_paths = np.hstack(file_paths)

    return file_paths

def filepath_check(file_location_paths): 
    """
    Check if file_location_paths is a single file or
    a directory. If a directory, unpack all file paths in a 
    folder and subfolders. 
    
    Arguments
    ---------
    file_location_paths (list or str): 


    Returns
    -------


    """

    # check if file or directory
    isFile = os.path.isfile(file_location_paths)
    isDirectory = os.path.isdir(file_location_paths)

    # directory search 
    file_paths = []
    if (isFile == False) and (isDirectory == True): 
        list_files = os.listdir(file_location_paths)
        
        for file_selected in list_files: 
            file_path = (os.path.join(file_location_paths, file_selected)) 

            # if there are still dir to unpack
            # search and unpack subfolders
            if os.path.isdir(file_path): 
                for root, dirs, files in os.walk(file_path):
                    for file in files:
                        file_paths.append(os.path.join(root,file))
            else: 
                file_paths.append(file_path)

    # single file search
    else: 
        file_paths.append(file_location_paths)

    return np.array(file_paths)

def abf_filepath_check(file_paths): 
    """
    Filter and return only file paths 
    to *.abf files. 
    """

    abf_file_paths = []
    for file_selected in file_paths: 
        if np.char.endswith(file_selected, ".abf"):
            abf_file_paths.append(file_selected)
        
    if len(abf_file_paths) == 0: 
        raise NoAbfFilesFound("No *.abf files found") # raise error

    return abf_file_paths

