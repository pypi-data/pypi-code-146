"""
loader.py

Data and metadata loader for action potential files. 

"""

import numpy as np
import pandas as pd

from itertools import chain

from ..abf.abf_obj import ABF
from ..utils.paths.find_paths import file_extensionfilt
from ..utils.reports.strings import (gen_ap_overview_str, gen_psc_overview_str)

###################################################################################################
###################################################################################################

def load(file_path = None, protocol = None): 
    """
    Returns action potential object containing
    instances of metadata and data (voltages, currents, times).   
    
    Arguments
    ---------
    file_path (str, list or arr): 
        paths to action potential files. 
        note: *.abf files only accepted.  
    
    Raises
    ------
    TypeError: 
        file paths type is not np.ndarray, list or a str
        
    KeyError: 
        no key file_path found in metadata dict 
        
    Examples
    --------
    >> data[3].metadata['file_path'] -- file path for loaded file 4
    >> data[0].voltages -- voltages for loaded file 1
    >> data[1].currents -- currents for loaded file 2
    
    """

    if file_path is not None: 
        
        #####################################
        # find file paths & return abf_object
        #####################################
        
        # unpack list
        #-------------
        # if a list of objects, 
        # metadata, strs or a combination
        # unpack and return abf objects
        
        abf_objects = []
        if isinstance(file_path, list): 
            
            # reduce nested list
            #--------------------
            if [x for x in file_path if type(x)== list]:
                nested = list(chain.from_iterable([x for x in file_path if type(x)== list]))
                try:
                    abf_objects = [x for x in nested if type(x)== ABF]
                except: 
                    raise TypeError("can not unpack a nested file path"
                                    f"list | {file_path}...")           
            else: 
                pass
            
            # find passed abf objects 
            #------------------------
            try: 
                abf_objects += [x for x in file_path if type(x)== ABF] 
            except: 
                pass
            
            # find passed metadata
            #---------------------
            try: 
                metadata = [x for x in file_path if type(x)== dict] 
                for i in range(len(metadata)): 
                    abf_objects.append(ABF(metadata[i]['file_path'], protocol = protocol)) 
            except: 
                pass
            
            # find all file paths
            #---------------------
            try: 
                metadata = [x for x in file_path if type(x)== str] 
                for file in file_extensionfilt([x for x in file_path if type(x)== str], extension = '.abf'):
                    abf_objects.append(ABF(file, protocol = protocol))
            except: 
                pass
            
        # abs paths
        #-----------
        elif isinstance(file_path, str): 
            
            for file in file_extensionfilt(file_path, extension = '.abf'): 
                abf_objects.append(ABF(file, protocol = protocol))
                
        # file paths in df 
        #------------------
        elif isinstance(file_path, pd.DataFrame): 
            
            try: 
                for file in file_path.loc[:, 'file_path']: 
                    abf_objects.append(ABF(file, protocol = protocol))
            except: 
                pass
            
        # abf object 
        #------------
        elif isinstance(file_path, ABF): 
            pass

        else: 
            raise TypeError(
                            "file_path must be a list, str,"
                            "metadata dict or ABF object | check type ..."
                            )

        # print summary 
        #---------------
        if protocol == 'ap': 
            print(gen_ap_overview_str(abf_objects)) 
        elif protocol == 'psc': 
            print(gen_psc_overview_str(abf_objects)) 
        else: 
            print(f'no loader summary | no protocol selected: {protocol}')
            
        return abf_objects
    
    else:
        raise ValueError("pass a file_path ...")