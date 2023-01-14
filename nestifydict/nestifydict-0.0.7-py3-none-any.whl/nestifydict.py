"""
A tool for parsing structured data (primarily nested dictionaries from json files). In particular it can flatten dictionaries, map flattened dicts to a template, and recursively get/set elements in nested dictionaries without a priori knowledge of the structure.
"""
__license__ = "BSD-3"
__docformat__ = 'reStructuredText'
__author__ = "Jared Beard"

import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from collections.abc import Iterable
from copy import deepcopy

__all__ = ["merge", "unstructure", "structure", "find_key", "recursive_set", "recursive_get"]

def merge(d_default : dict, d_merge : dict, do_append : bool = False):
    """
    Adds d_merge values to d_default recursively. 
    Values in d_merge overwrite those of d_default values, 
    however nonexistent values in d_default are retained, 
    which differs from use of {**d_base, **d_merge}

    :param d_default: (dict) base dictionary
    :param d_merge: (dict) dictionary to add
    :param do_append: (bool) if true, will append iterable elements of not dict type, *default*: Flase
    :return: (dict) combined dictionary
    """
    d_default = deepcopy(d_default)
    for key in d_merge:
        if key not in d_default: 
            d_default[key] = deepcopy(d_merge[key])
        else:
            if isinstance(d_default[key],dict) and isinstance(d_merge[key],dict):
                d_default[key] = merge(d_default[key], d_merge[key], do_append)
            elif isinstance(d_merge[key], Iterable) and type(d_default[key]) == type(d_merge[key]):
                d_default[key] += d_merge[key]
            else:
                d_default[key] = deepcopy(d_merge[key])

    return d_default
    
def unstructure(d):
    """
    Flattens nested dictionary (if keys are used multiple places, they will be overwritten)
            
    :param d: (dict) dictionary to flatten
    :return: (dict) keys and values for each element in d
    """
    if isinstance(d, dict):
        d_new = {}
        for key in d:
            d_temp = unstructure(d[key])
            if None in d_temp:
                d_temp[key] = d_temp.pop(None,d_temp[None])  
            d_new.update(d_temp)
        return d_new         
    else:
        return {None: d}
        
def structure(d_flat : dict, d_structure : dict, reject_nonexistent : bool = True):
    """
    Maps dictionary to a preferred structure 
    
    **This will consume d_flat**

    :param d_flat: (dict) dict containing values
    :param d_structure: (dict) dictionary containing structure and default values
    :param reject_nonexistent: (bool) If true, keys of d_flat not in d_structure will be thrown out, *default*: True
    :return: Structured dictionary
    """
    d_out = deepcopy(d_structure)
    for key in d_structure:
        if isinstance(d_structure[key], dict):
            d_out[key] = structure(d_flat, d_structure[key])
        elif key in d_flat:
            d_out[key] = deepcopy(d_flat[key])
            d_flat.pop(key)
            
    if not reject_nonexistent:
        d_out.update(d_flat)

    return deepcopy(d_out)

def find_key(d : dict, key):
    """
    Finds first instance of key in nested dict
    
    :param d: (dict) dictionary to search
    :param key: () key
    :return: (list) Returns order of keys to access element or None if nonexistent
    """
    if key not in d:
        for k, val in d.items():
            if isinstance(val, dict):
                key = find_key(val,key)
                if isinstance(key,list):
                    return [k] + key
    else:
        return [key]
    return None
    
def recursive_set(d : dict, key : list, val, as_hint = False):
    """
    Updates dictionary value given an ordered list of keys.
    Can also support keys as hints and will search for the *first* key before attempting to set it.
    (Later may update find_key to match a list of keys or make a find_key_list function)
    In either case, if key is not found it will be added to root
    
    :param d: (dict) dictionary to update
    :param key: (list) list of keys
    :param val: () value
    :param as_hint: (bool) if true, attempts to find key before setting it, *default*: False
    """
    if as_hint and key[0] not in d:
        temp_key = find_key(d, key[0])
        if isinstance(temp_key, list):
            key = temp_key + key[1:len(key)]
        recursive_set(d,key,val)
    else:
        if len(key) > 1:
            if key[0] not in d or (not isinstance(d[key[0]], dict)):
                d[key[0]] = {}
            recursive_set(d[key[0]], key[1:len(key)], val)
        else:
            d[key[0]] = val
            
def recursive_get(d : dict, key : list):
    """
    Returns value from dict recursive key
    
    :param d: (dict) dictionary containing key
    :param key: (list) list of keys
    :return: () Value
    """
    if not isinstance(key,list):
        return d[key]
    if len(key) == 1:
        return d[key[0]]
    return recursive_get(d[key[0]],key[1:len(key)])