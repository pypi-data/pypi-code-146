"""
ap_metadata_filter.py 

Filter metadata.
"""

# ap loader 
import brainspike.ap.loader as ap_loader

# ap metadata
import brainspike.ap.metadata as metadata_loader

# libraries
import os
import numpy as np
import pandas as pd
from datetime import date, timedelta

# error raise
class NotAList(Exception): pass
class MultipleInputs(Exception): pass

#----------------------------------------

######################
# filter abf metadata
######################

# separate this out into ap_metadata_filter!!!!! 
# place in a check --> see https://ipfx.readthedocs.io/en/latest/_modules/ipfx/x_to_nwb/ABFConverter.html

# place this all into static method abf_ap_metadata_filter? 
# what if the df is only two variables? Ie no df? --> add this in! 
# need to make options to filter between a range but also just select multiple at a time! 
# need to do this for all!!! including file_path and abf_id ... 
# add a range of abf_ids here
# add a range for abf_id filtering 
# change the name of general filter function?
# write all doc_strings here
# place an int check in for the metadata filtering
# conduct a metadata check here!!!!!!!! or split into _check ... 


def filter(metadata, abf_id = None, file_path = None, date = None, date_range = None, time_of_recording = None, time_of_recording_range = None,\
    current_step_pa = None, current_step_pa_range = None, max_current_injected_pa = None, max_current_injected_pa_range = None,\
         min_current_injected_pa = None, min_current_injected_pa_range = None, sample_rate_hz = None, sample_rate_hz_range = None, sweep_length_sec = None,\
              sweep_length_sec_range = None, channel_count = None, channel_count_range = None, datalength_min = None, datalength_min_range = None,\
                   sweep_count = None, sweep_count_range = None, channel_list = None, channel_list_range = None, file_comment = None, tag_comment = None,\
                        abf_version = None): 

    """
    Currently set for abf metadata outputs. 

    Arguments
    ---------

    ** to finish ** 

    Returns
    -------


    """

    return_object = False

    # parse metadata list of objects 
    if isinstance(metadata, list):
        metadata = metadata_loader.get_metadata(metadata)
        return_object = True 

    # filter each variable
    abf_ids = check_type(metadata, abf_id, 'abf_id') # no range option
    file_paths = check_type(metadata, file_path, 'file_path') # no range option
    dates = filter_dates(metadata, date, date_range)
    recording_times = filter_times(metadata, time_of_recording, time_of_recording_range) 
    current_steps = filter_values(metadata, 'current_step_pa', current_step_pa, current_step_pa_range)
    min_current_steps = filter_values(metadata, 'min_current_injected_pa', min_current_injected_pa, min_current_injected_pa_range)
    max_current_steps = filter_values(metadata, 'max_current_injected_pa', max_current_injected_pa, max_current_injected_pa_range)
    sample_rates = filter_values(metadata, 'sample_rate_hz', sample_rate_hz, sample_rate_hz_range)
    sweep_lengths = filter_values(metadata, 'sweep_length_sec', sweep_length_sec, sweep_length_sec_range)
    channel_counts = filter_values(metadata, 'channel_count', channel_count, channel_count_range)
    datalengths = filter_values(metadata, 'datalength_min', datalength_min, datalength_min_range)
    sweepcounts = filter_values(metadata, 'sweep_count', sweep_count, sweep_count_range)
    channel_lists = filter_values(metadata, 'channel_list', channel_list, channel_list_range)
    file_comments = check_type(metadata, file_comment, 'file_comment') # no range option
    tag_comments = check_type(metadata, tag_comment, 'tag_comment') # no range option
    abf_versions = check_type(metadata, abf_version, 'abf_version') # no range option

    # filter metadata df columns
    metadata = metadata.loc[metadata.file_path.isin(file_paths) & metadata.date.isin(dates) & metadata.current_step_pa.isin(current_steps) &
    metadata.time_of_recording.isin(recording_times) & metadata.max_current_injected_pa.isin(max_current_steps) & metadata.min_current_injected_pa.isin(min_current_steps)
    & metadata.sample_rate_hz.isin(sample_rates) & metadata.sweep_length_sec.isin(sweep_lengths) & metadata.channel_count.isin(channel_counts)
    & metadata.datalength_min.isin(datalengths) & metadata.sweep_count.isin(sweepcounts) & metadata.channel_list.isin(channel_lists) & metadata.file_comment.isin(file_comments)
    & metadata.tag_comment.isin(tag_comments) & metadata.abf_version.isin(abf_versions)]

    # filter metadata df index 
    metadata = metadata.filter(items = abf_ids, axis = 0) 

    if return_object == True: 
        return metadata_loader.get_objects_from_metadata(metadata)
    else: 
        return metadata


def filter_dates(metadata, date, date_range): 
    """
    Filter dates if a single value. 
    Create a range of values if date_range parsed. 
    
    Arguments
    ---------


    Returns
    -------


    """

    if (date == None) and (date_range != None): # range of dates between list values
        if isinstance(date_range, list): 
            if len(date_range) == 2: 
                date_filt = get_dates(date_range) # filter between dates
            elif len(date_range) == 1:
                date_filt = check_type(metadata, date[0], var = 'date')
            elif len(date) > 2: 
                raise NotAList("A list of 2 values needed to filter a range of dates")
        else: 
            raise NotAList("A list of 2 values needed to filter a range of dates")

    if (date != None) and (date_range == None):  
        date_filt = check_type(metadata, date, var = 'date')
    if (date == None) and (date_range == None):  
        date_filt = metadata.date.values
    if (date != None) and (date_range != None): 
        raise MultipleInputs("Check: multiple date inputs")

    return date_filt


def filter_times(metadata, time_of_recording, time_of_recording_range): 
    """
    Filter times if a single value. 
    Create a range of times if date_range parsed. 
    Note: list of times (list; "%H:%M:%S").
    
    Arguments
    ---------


    Returns
    -------


    """

    if (time_of_recording == None) and (time_of_recording_range != None): # range of dates between list values
        if isinstance(time_of_recording_range, list): 
            if len(time_of_recording_range) == 2: 
                time_of_recording_filt = get_times(time_of_recording_range) # filter between times
            elif len(time_of_recording_range) == 1:
                time_of_recording_filt = check_type(metadata, time_of_recording_range[0], var = 'time_of_recording')
            elif len(time_of_recording_range) > 2: 
                raise NotAList("A list of 2 values needed to filter a range of recording times")
        else: 
            raise NotAList("A list of 2 values needed to filter a range of recording times")

    if (time_of_recording != None) and (time_of_recording_range == None):  
        time_of_recording_filt = check_type(metadata, time_of_recording, var = 'time_of_recording')
    if (time_of_recording == None) and (time_of_recording_range == None):  
        time_of_recording_filt = metadata.time_of_recording.values
    if (time_of_recording != None) and (time_of_recording_range != None): 
        raise MultipleInputs("Check: multiple date inputs")

    return time_of_recording_filt


def filter_values(metadata, var, values, value_range): 
    """
    
    """

    # if no range of values selected
    # return list or str inputs 
    if (values != None) and (value_range == None): 
        filtered_values = check_type(metadata, values)

    # if a list of 2 value parsed
    # get range of values between 
    elif (values == None) and (value_range != None): 
        if var == 'sweep_length_sec': 
            filtered_values = get_values(value_range, var) # decrease step 
        else: 
            filtered_values = get_values(value_range)

    # if no filtering
    # default to all values for 'var' selected
    elif (values == None) and (value_range == None): 
        filtered_values = metadata.loc[:, var].values # search for all values (default)

    # raise error if multiple inputs 
    elif (values != None) and (value_range != None): 
        raise MultipleInputs("Multiple current_step_pa inputs")

    return filtered_values


def check_type(metadata, value, var = None): 
    """
    Check the type of value parsed for filtering (list of str). 
    Return a list of values for filtering metadata. 

    Arguments
    ---------


    Returns
    -------
    
    """

    # str
    if (value is not None) and (isinstance(value, str) == True) and (isinstance(value, list) == False):
        if var in ('date', 'abf_id', 'file_comment', 'file_path', 'time_of_recording', 'abf_version', 'tag_comment'): 
            filtered_values = [value] 

        elif isinstance(int(float(value)), int) == True: # else convert str to int 
            filtered_values = [int(float(value))]

    #------
    # list 
    if (value is not None) and (isinstance(value, str) == False) and (isinstance(value, list) == True):
        # check if list of numbers
        if var not in ('abf_id', 'date', 'time_of_recording', 'tag_comment', 'file_comment', 'abf_version'): 
            if (all([isinstance(item, int) for item in value])) == False:
                filtered_values = [int(float(item)) for item in value] # convert to int if str 
            else: 
                filtered_values = value
        else: 
            filtered_values = value

    #------
    # float
    if (value is not None) and (isinstance(value, float) == True):
        filtered_values = [value]

    #------
    # int
    if (value is not None) and (isinstance(value, int) == True):
        filtered_values = [value]

    #------
    # default to all values
    # if none
    if value == None: 
        if var == 'abf_id': 
            filtered_values = metadata.index.values # set_index as abf_id
        if var == 'file_comment': 
            filtered_values = metadata.loc[:, var].values # file comment blanks 
        if var != 'abf_id' and var != 'file_comment': 
            filtered_values = metadata.loc[:, var].values 

    return filtered_values


def get_values(value_range, var = None): 
    """
    
    """

    if var == 'sweep_length_sec': 
        step = 0.001 # 1 ms step for improved filtering
    else: 
        step = 1

    if isinstance(value_range, list):
        if len(value_range) == 2: 
            values = np.arange(value_range[0], value_range[1]+1, step)
        elif len(value_range) == 1:
            values = check_type(value_range[0])   
        elif len(value_range) > 2: 
            raise NotAList(f"A list of 2 values needed for {var} range filtering")  
    else: 
        raise NotAList(f"A list of 2 values needed for {var} range filtering")

    return values


def get_dates(date_range): 
    """
    Return a list of dates between two values. 

    Arguments
    --------- 
    date_range (list): 


    Returns
    -------


    """

    if isinstance(date_range, list): 
        
        if len(date_range) == 2: 
            for x in range(2): 
                val = date_range[x].replace('-', ' ')
                val = val.split(' ')
                val = list(map(int, val)) 
                
                if x == 0: 
                    start_date = date(val[0], val[1], val[2]) # find dates 
                if x == 1: 
                    end_date = date(val[0], val[1], val[2])
                    
            days = pd.date_range(start = start_date, end = end_date, freq='D') # create range of dates
        else: 
            raise NotAList("List of 2 values needed")
    else: 
        raise NotAList("Parse a list")
    
    return days.strftime('%Y-%m-%d').values


def get_times(time_range): 
    """
    Return a list of times between two values. 
    Range is per second (not millisecond). 

    Arguments
    --------- 
    time_range (list; "%H:%M:%S"): 


    Returns
    -------


    """

    if isinstance(time_range, list): 
        if len(time_range) == 2: 
            time = pd.date_range(start = time_range[0], end = time_range[1], freq="s") # create range of dates

        else: 
            raise NotAList("List of 2 values needed")
    else: 
        raise NotAList("Parse a list")

    return time.strftime("%H:%M:%S")