"""
ap_output.py

Output processed data, metadata and processed
in memory objects. 
"""

# libaries
import os
import json 

# numpy
import numpy as np

# pandas
import pandas as pd

# error raise
class DataTypeError(Exception): pass
class FileIdTypeError(Exception): pass

#----------------------------

def output_reportsummary(data, fname = None, add_metadata = True): 
    """
    Export report summary as .json, .xlsx or .csv file. 
    Attach or remove metadata (default: True). 

    Arguments
    ---------


    Returns
    -------


    """

    data = check_type(data) # type check for numpy or ap_objects
    
    df = pd.DataFrame()
    metadata_all = []
    report_summary_all = []
    
    for x in range(len(data)): 
        metadata_all.append(data[x].metadata)
        report_summary_all.append(data[x].report_summary)

    if add_metadata == True: 
        df = pd.concat([pd.concat(metadata_all), pd.concat(report_summary_all)], axis = 1)

    if add_metadata == False: 
        df = pd.concat(report_summary_all)

    if fname != None: 
        save(fname, df) # save

    return df


def output_spikefeatures(data, fname = None, file_id = None): 
    """
    
    Arguments
    ---------


    Returns
    -------

    """

    data = check_type(data) # type check for numpy or ap_objects    

    spikes_features_all = []
    identifier = []

    for x in range(len(data)): 
        identifier.append(np.repeat(data[x].metadata.index.values[0], len(data[x].spikes_features)))
        spikes_features_all.append(data[x].spikes_features)
        
    df = pd.concat(spikes_features_all)
    df['identifier'] = np.concatenate(identifier, axis = 0)
    df = df.set_index('identifier')

    if file_id != None:
        if isinstance(file_id, list):     
            df = df[df.index.isin(file_id)] # selected file_id isolation
        elif isinstance(file_id, str):    
            df = df[df.index == file_id]
        else: 
            raise FileIdTypeError("parse a list of strings or a single string to subselect for file_ids")

    if fname != None: 
        save(fname, df) # save

    return df

def output_sweepfeatures(data, fname = None, file_id = None): 
    """

    Arguments
    ---------


    Returns
    -------
    
    """

    data = check_type(data) # type check for numpy or ap_objects    

    sweeps_features_all = []
    identifier = []

    for x in range(len(data)): 
        identifier.append(np.repeat(data[x].metadata.index.values[0], len(data[x].sweeps_features)))
        sweeps_features_all.append(data[x].sweeps_features)
        
    df = pd.concat(sweeps_features_all)
    df['identifier'] = np.concatenate(identifier, axis = 0)
    df = df.set_index('identifier')

    if file_id != None:
        if isinstance(file_id, list):     
            df = df[df.index.isin(file_id)] # selected file_id isolation
        elif isinstance(file_id, str):    
            df = df[df.index == file_id]
        else: 
            raise FileIdTypeError("parse a list of strings or a single string to subselect for file_ids")

    if fname != None: 
        save(fname, df) # save

    return df


#---------------------------------------

def save(fname, df): 
    """

    Arguments
    ---------


    Returns
    -------
    
    
    """

    #---------------------------------------
    # find file name search for file path
    filename_idx = (fname.rfind('/'))
    if filename_idx: 
        filename = fname[filename_idx+1:]
        create_path(fname[:filename_idx])
    else: 
        filename = fname # no path parsed

    # find filename extension
    file_extension_idx = (filename.rfind('.'))
    file_extension = filename[file_extension_idx:]
    
    #---------------------------------------
    # save file out 
    if file_extension == '.xlsx': 
        df.to_excel(fname)

    elif file_extension == '.csv': 
        df.to_csv(fname) 

    elif file_extension == '.json': 
        json_out_file = open(fname, "w") 
        json.dump(df.reset_index().to_json(), json_out_file, indent = 6) 
        json_out_file.close() 

    # elif file_extension == '.txt': 
    #     df.to_csv(filename, header=None, index=None, sep='\t', mode='a')

        ## to re-import json as df
        # f = open('analysed/test/report_summary_nometadata.json')
        # data1 = json.load(f) # returns JSON object as a dictionary
        # df = pd.read_json(data1) # converting it into dataframe

    else: 
        raise DataTypeError("save filename as either .xlsx, .csv, .json or .txt")


def create_path(filename): 
    """
    Creates path and directory to dataframes (if does not exist) within a set subfolder 
    and with a filename. 
    
    Arguments
    ---------
    fiename (str): 
        path to file
    
    Returns
    -------
    Creates directory and outputs file path for saving as specified format
    """

    isExist = os.path.exists(filename) 
    if not isExist:
        os.makedirs(filename)
        print(f"The new directory is created for {filename}")

#--------------------

def check_type(data): 
    """
    
    Arguments
    ---------


    Returns
    -------

    ** repeated from other function -> put this is a wrapper? **
    ** OR: import ap_processing.py method? ** 
    """

    if isinstance(data, list): 
        if len(data) > 0: 
            if type(data[0]) != list or int or str or pd.DataFrame: # unpack first ap_object only
                return data
            else: 
                raise DataTypeError("Wrong data type | parse a list of ap_objects processed using ap_loader")
        else: 
            raise DataTypeError("No data found")

    elif isinstance(data, np.ndarray): 
         raise DataTypeError("Wrong data type | parse a list of ap_objects processed using ap_loader")
    elif isinstance(data, dict): 
        raise DataTypeError("Wrong data type | parse a list of ap_objects processed using ap_loader")
    elif isinstance(data, pd.DataFrame): 
        raise DataTypeError("Wrong data type | parse a list of ap_objects processed using ap_loader")
    elif isinstance(data, str):
        raise DataTypeError("Wrong data type | parse a list of ap_objects processed using ap_loader")
    elif isinstance(data, int):
        raise DataTypeError("Wrong data type | parse a list of ap_objects processed using ap_loader")
