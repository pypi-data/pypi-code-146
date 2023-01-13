"""
abf_ap_loader.py

Michael Zabolocki, Aug 2022

Child class for .abf action potential files. 
"""

# file path load
import brainspike.ap.loader as ap_loader

# data extraction
from brainspike.ap.abf.data import AbfApData

# metadata extraction
from brainspike.ap.abf.metadata import AbfApMetadata

# tqdm
from tqdm import tqdm as tqdm 

# numpy
import numpy as np

# import libraries
import types

# error raise 
class CurrentCheck(Exception): pass

#-----------------------------

def load(file_paths, metadata_out = True, lowpass_cutoff = None, filter_order = None, win_len = None): 
    """
    
    Returns
    -------



    Arguments
    ---------

    
    """
    
    pbar = tqdm(total=100, desc = 'Processed files', colour="blue", position=0, leave=True, mininterval=0) # progress bar 

    abf_objects = []

    for file_selected in file_paths: 
        if np.char.endswith(file_selected, ".abf"): # safety check

            pbar.update(100/len(file_paths)) # pbar update

            # create abf object 
            abf_object = types.SimpleNamespace()

            #--------------
            # add v,t,and stimulus arrays per sweep to object
            data = AbfApData(file_selected, lowpass_cutoff, filter_order, win_len)
            abf_object.time = data.time
            abf_object.voltage = data.voltage
            abf_object.stimulus = data.stimulus

            #--------------
            # current steps
            current_steps, currentinj_start_end = get_currentsteps(data.stimulus)
            abf_object.currentinj_start_end = currentinj_start_end
            abf_object.current_steps = current_steps

            #--------------
            # get metadata
            metadata_obj = AbfApMetadata(file_selected, current_steps, lowpass_cutoff, filter_order, win_len, metadata_out)
            abf_object.metadata = metadata_obj.metadata_df

            #--------------
            # append abf_objects
            abf_objects.append(abf_object)
            
    pbar.close()

    return abf_objects


def get_currentsteps(stimulus): 
    """
    
    Arguments
    ---------

    Returns
    -------


    """

    # current steps
    step_calc_max = np.amax(stimulus, axis=1) # max current injection (+ve polarity)
    step_calc_min = np.amin(stimulus, axis=1) # min current injection (-ve polarity) 
    current_steps = step_calc_max - abs(step_calc_min)  # current delta 
    # idx of current injection 
    #   calculated for first sweep with positiv current input
    #   --> (pClamp software for *.abf generation defaults to zero if recording stopped midway)
    positive_currentsteps = np.where(current_steps > 0)

    if len(positive_currentsteps) > 0: 
        currentinj_start_end = np.where(stimulus[positive_currentsteps[0][0]] == current_steps[positive_currentsteps[0][0]])
    else: 
        raise CurrentCheck("No positive current stimulus applied | check stimulus")

    #--------------
    # add to self
    currentinj_start_end = currentinj_start_end
    current_steps = current_steps

    return current_steps, currentinj_start_end



        




