"""
check_paths.py

Modules to check if abs paths and dir exist. 

"""

import os 
import numpy as np

###################################################################################################
###################################################################################################

def check_dir_abs(file_loc = None): 
    """
    Check if path is a abs path or a directory.
    If a directory, unpack all file paths in a folder and subfolders. 
    
    Arguments
    ---------
    file_loc (list or str): 
        location of file (dir or abs path)

    Returns
    -------
    Unpacks and returns all file paths. 
    
    Raises
    ------
    NoFilePathFound:
        can not find any file paths in the dir passed. 

    """

    if file_loc is not None: 
        
        isFile = os.path.isfile(file_loc)
        isDirectory = os.path.isdir(file_loc)

        # search dir
        file_paths = []
        if (isFile == False) and (isDirectory == True): 
            list_files = os.listdir(file_loc)
            
            for file_selected in list_files: 
                file_path = (os.path.join(file_loc, file_selected)) 

                # if dir to unpack search subfolder
                if os.path.isdir(file_path): 
                    for root, dirs, files in os.walk(file_path):
                        for file in files:
                            file_paths.append(os.path.join(root,file))
                else: 
                    file_paths.append(file_path)
        else: 
            file_paths.append(file_loc)

        return np.array(file_paths)
    
    else: 
        raise FileNotFoundError(f"pass file paths | {file_loc}")
