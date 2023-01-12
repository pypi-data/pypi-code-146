# Code Mixed Text Toolkit
"""
Functions to load local and online resource files, list and download CMTT datasets.
"""

import pickle
import json
import pandas as pd
from urllib.request import urlopen
import os

from cmtt.data.downloader import download_dataset_url, download_cmtt_datasets

AUTO_FORMATS = {
  "pickle": "pickle",
  "json": "json",
  "txt": "text",
  "text": "text",
  "csv": "csv",
  "conll": "conll"
}

FORMATS = {
  "pickle": "A serialized python object, stored using the pickle module.",
  "json": "A serialized python object, stored using the json module.",
  "text": "The raw (unicode string) contents of a file.",
  "csv": "A serialized python object, stored using the pandas module.",
  "conll": ""
}

def load_url(
  resource_url,
  format="auto",
  encoding=None):

  '''suported resource formats:
    -"txt"
    -"csv"
    -"pickle"
    -"json"
    -"raw"
  '''
  
  # Determine the format of the resource.
  if format == "auto":
    resource_url_parts = resource_url.split(".")
    ext = resource_url_parts[-1]
    if ext == "gz":
      ext = resource_url_parts[-2]
    format = AUTO_FORMATS.get(ext)
    if format is None:
      raise ValueError(
        "Could not determine format for %s based "
        'on its file\nextension; use the "format" '
        "argument to specify the format explicitly." % resource_url
      )
  
  if format not in FORMATS:
    raise ValueError(f"Unknown format type: {format}!")

  # Load the resource using URL.
  opened_resource = urlopen(resource_url)

  if format == "raw":
    resource_val = opened_resource.read()
  elif format == "pickle":
    resource_val = pickle.load(opened_resource)
  elif format == "json":
    resource_val = json.load(opened_resource)
  elif format == "csv":
    resource_val = pd.read_csv(opened_resource)
  else:
    # The resource is a text format.
    binary_data = opened_resource.read()
    if encoding is not None:
      string_data = binary_data.decode(encoding)
    else:
      try:
        string_data = binary_data.decode("utf-8")
      except UnicodeDecodeError:
        string_data = binary_data.decode("latin-1")
    if format == "text":
      resource_val = string_data

  opened_resource.close()
  return resource_val

def load_local(
  resource_path,
  format="auto",
  encoding=None):

  '''suported resource formats:
    -"txt"
    -"csv"
    -"pickle"
    -"json"
    -"raw"
    -"conll"
  '''
  
  # Determine the format of the resource.
  if format == "auto":
    resource_path_parts = resource_path.split(".")
    ext = resource_path_parts[-1]
    if ext == "gz":
      ext = resource_path_parts[-2]
    format = AUTO_FORMATS.get(ext)
    if format is None:
      raise ValueError(
        "Could not determine format for %s based "
        'on its file\nextension; use the "format" '
        "argument to specify the format explicitly." % resource_path
      )
  
  if format not in FORMATS:
    raise ValueError(f"Unknown format type: {format}!")

  # Load the resource using URL.
  opened_resource = open(resource_path, 'rb')

  if format == "raw":
    resource_val = opened_resource.read()
  elif format == "pickle":
    resource_val = pickle.load(opened_resource)
  elif format == "json":
    resource_val = json.load(opened_resource)
  elif format == "csv":
    resource_val = pd.read_csv(opened_resource)
  else:
    # The resource is a text format.
    binary_data = opened_resource.read()
    if encoding is not None:
      string_data = binary_data.decode(encoding)
    else:
      try:
        string_data = binary_data.decode("utf-8")
      except UnicodeDecodeError:
        string_data = binary_data.decode("latin-1")
    if format == "text":
      resource_val = string_data
    if format == "conll":
      resource_val = string_data
  opened_resource.close()
  return resource_val


def list_dataset_keys():
  """
    Returns the list of key prperties of the datasets provided by the cmtt library
    :return: list of keys
    :rtype: list
  """

  path = os.path.dirname(os.path.realpath(__file__))
  f = open(os.path.join(path, "data.json"))
  data = json.load(f)
  f.close()
  return list(data['datasets'][0].keys())

def list_cmtt_datasets(search_key="all", search_term = "", isPrint=False):
  """
    Returns the list the datasets provided by the cmtt library.
    :param search_key: dataset property in which the search_term is to searched. 
    :type key: str
    :param search_term: term to be search in the list of datasets
    :type key: str
    :param print: turn on and off the print statemnet
    :type isPrint: bool
    :return: list of datasets with the property key
    :rtype: list
  """

  path = os.path.dirname(os.path.realpath(__file__))
  f = open(os.path.join(path, "data.json"))
  data = json.load(f)
  if isPrint:
    print("Total available datasets: " + str(len(data['datasets'])))
    print("Following are the datasets based on the search parameters: ")

  # if(key=="name" or key=="all"):
  #   lst = []
  # else:
  #   lst = {}

  # if(key=="all"):
  #   for i in data['datasets']:
  #     lst.append(i)
  #     if isPrint:
  #       print(i)
  # elif(key in data['datasets'][0].keys()):
  #   for i in data['datasets']:
  #     if(key != 'name'):
  #       lst[i['name']] = i[key]
  #     else:
  #       lst.append(i[key])
  #   if isPrint:
  #     print("Key: " + key + "\n" + str(lst))
  # else:
  #   print("The key " + key + " is not a valid key")
  #   print("Valid keys: " + str(data.keys()))

  # f.close()
  # return lst

  datasets = data['datasets']
  dataset_list = []
  if(search_key == "all"):
    for i in datasets:
      if(search_term != ""):
        values = [x.lower() for x in i.values()]
        for val in values:
          if search_term.lower() in val:
            dataset_list.append(i)
            break
      else:
        dataset_list.append(i)
  else:
    dataset_keys = list_dataset_keys()
    if search_key in dataset_keys:
      for i in datasets:
        if(search_term != ""):
          if search_term.lower() in i[search_key].lower():
            dataset_list.append(i)
        else:
          dataset_list.append(i)
    else:
      raise KeyError("Invalid key.")

  f.close()
  if isPrint:
    for i in dataset_list:
      print(json.dumps(i, sort_keys=True, indent=4))
      print()
  return dataset_list