"""
find_paths.py

Modules to find abs paths and dirs. 

"""

import numpy as np

from . check_paths import check_dir_abs

class NoFilePath(Exception): pass

###################################################################################################
###################################################################################################

def all(path = None): 
    """
    Find all file paths and check if they exist.
    If dir found, unpacks all subfolders. 

    Arguments
    ---------
    path (str or list):
        path(s) to dir. 
    
    Returns
    -------
    Returns arr of unique file paths in dir. 
    
    Raises
    ------
    FileNotFoundError:
        can not find any file paths in the dir passed. 
    
    """

    if isinstance(path, str): # load all abs paths

        file_paths = check_dir_abs(path) 

        if len(file_paths) == 0: 
            raise FileNotFoundError("no file paths found ...") 

    if isinstance(path, list) | isinstance(path, np.ndarray): # list or ndarray input

        file_paths = []
        for file_dir in path: 
            file_paths.append(check_dir_abs(file_dir)) 
            
        if len(file_paths) == 0: 
            raise FileNotFoundError("no file paths found ...") 
        else: 
            file_paths = np.hstack(file_paths) # arr conv
            file_paths = np.unique(file_paths, axis=0) # remove dup

    return file_paths


def file_extensionfilt(file_paths, extension = '.abf'): 
    """
    Find all file paths. Filter and return only file paths
    for selected file extension. Default set to '*.abf'. 
    
    Arguments
    ---------
    file_paths (list or arr): 
        file paths to filter for extension type. 

    extension (str):    
        file extension (default: *.abf). 
    
    Returns
    -------
    Returns list of file paths with selected file extension
    from passed arr. 
    
    Raises
    ------
    FileNotFoundError:
        can not find any file paths in the dir passed. 
    
    """
    
    file_paths = all(file_paths) # find all 

    selected_file_paths = []
    for file_selected in file_paths: 
        if np.char.endswith(file_selected, extension):
            selected_file_paths.append(file_selected)
        
    if len(file_paths) == 0: 
        raise FileNotFoundError(f"no files with {extension} extension found ...") 
    else:
        pass

    return selected_file_paths