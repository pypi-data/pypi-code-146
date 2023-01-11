"""
memory_ap_transformer.py

Michael Zabolocki, Oct 2022

Convert in memory files (e.g. numpy) into an ap_object for further processing. 
"""

# numpy
import numpy as np

# pandas
import pandas as pd

# libraries
import types

# data extraction
from brainspike.ap.memory.data import MemoryApData

# metadata extraction
from brainspike.ap.memory.metadata import MemoryApMetadata

# error raise
class CheckError: pass
class CurrentCheck(Exception): pass

def load(times, stimuli, voltages, metadata, metadata_out): 
    """
    
    ** needs to input metadata for this manually then gives the option to export this ** 

    Returns
    -------



    Arguments
    ---------

    
    """
    if isinstance(metadata, dict): 
        metadata = pd.DataFrame(metadata)

    metadata = metadata.reset_index()

    #------------------
    memory_objects = []
    if len(times) == len(stimuli) == len(voltages): 

        if isinstance(times, np.ndarray) and isinstance(stimuli, np.ndarray) and isinstance(voltages, np.ndarray): 

            for num in range(len(voltages)): 
                
                #--------------
                # create empty memory object 
                memory_object = types.SimpleNamespace()

                #--------------
                # add v,t,and stimulus arrays per sweep to object
                data = MemoryApData(times[num], stimuli[num], voltages[num])
                memory_object.time = data.time
                memory_object.voltage = data.voltage
                memory_object.stimulus = data.stimulus

                #--------------
                # current steps
                current_steps, currentinj_start_end = get_currentsteps(data.stimulus)
                memory_object.currentinj_start_end = currentinj_start_end
                memory_object.current_steps = current_steps

                #--------------
                # get metadata
                metadata_obj = MemoryApMetadata(current_steps, metadata[metadata.index == num].copy(), metadata_out)
                memory_object.metadata = metadata_obj.metadata_df

                #--------------
                # append memory object
                memory_objects.append(memory_object)

        else: 
            raise CheckError(f"numpy.ndarray needed to be parsed")
            
    else: 
        raise CheckError(f"Check length of for ... time: {len(times)} | stimulus: {len(stimuli)} | voltage: {len(voltages)}")

    return memory_objects


def get_currentsteps(stimulus): 
    """
    Place this into a wrapper??? 
    This is repeated in the abf
    
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
