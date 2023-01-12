# Code Mixed Text Toolkit
# Download dataset given name (list) or url
# Save into folder corpora in C file
# Show progress in command line
# Download finished

import pickle
import os
import json
import pandas as pd
import urllib.request
import requests
from urllib.request import urlopen
from tqdm import tqdm
import zipfile
import platform

def download_file(url, destination, name, format):
  """
    Downloads a file from a url into the destination folder
    :param url: the source url of the dataset
    :type url: str
    :param destination: the destination path of the dataset to be downloaded
    :type destination: str
    :param name: name of the dataset at the destination folder
    :type name: str
    :param format: format of the dataset to be downloaded
    :type format: str
  """
  fname = destination
  response = requests.get(url, stream=True)
  total_size_in_bytes= int(response.headers.get('content-length', 0))
  block_size = 1024 #1 Kibibyte
  progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
  with open(fname, 'wb') as file:
    for data in response.iter_content(block_size):
      progress_bar.update(len(data))
      file.write(data)
  progress_bar.close()
  if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
    print("ERROR, something went wrong")
  else:
    print("\nDataset file successfully downloaded into path: " + destination)
    if (format == "zip"):
      print("Downloaded file is a zip file. Extracting zip file..")
      os.makedirs(os.path.join(os.path.dirname(destination), name))
      destination_after_extraction = os.path.join(os.path.dirname(destination), name)
      with zipfile.ZipFile(destination, 'r') as zip_ref:
          zip_ref.extractall(destination_after_extraction)
      os.remove(destination)
      print("Successfully extracted downloaded file into path: " + destination_after_extraction)
      return destination_after_extraction

    return destination

def download_file_from_google_drive(id, destination, name, format):
  """
    General method for downloading a file from Google Drive.
    Doesn't require using API or having credentials
    :param id: the source google drive file id of the dataset
    :type id: str
    :param destination: the destination path of the dataset to be downloaded
    :type destination: str
    :param name: name of the dataset at the destination folder
    :type name: str
    :param format: format of the dataset to be downloaded
    :type format: str
  """

  URL = "https://docs.google.com/uc?export=download"

  session = requests.Session()

  response = session.get(URL, params = { 'id' : id }, stream = True)
  token = get_confirm_token(response)

  if token:
    params = { 'id' : id, 'confirm' : token }
    response = session.get(URL, params = params, stream = True)

  return save_response_content(response, destination, name, format)    

def get_confirm_token(response):
  """
    Part of keep-alive method for downloading large files from Google Drive
    Discards packets of data that aren't the actual file
    :param response: session-based google query
    :return: either datapacket or discard unneeded data
  """

  # Download warning appears while trying to download large files from google drive
  for key, value in response.cookies.items():
    if key.startswith('download_warning'):
      return value

  return None

def save_response_content(response, destination, name, format):
  """
    Saves and writes the response data into the destination folder
    :param response: response after executing a get request
    :type response: requests.Response object
    :param destination: the destination path of the dataset to be downloaded
    :type destination: str
    :param name: name of the dataset at the destination folder
    :type name: str
    :param format: format of the dataset to be downloaded
    :type format: str
  """

  CHUNK_SIZE = 1024
  total_size_in_bytes= int(response.headers.get('content-length', 0))
  progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
  with open(destination, "wb") as f:
    for chunk in response.iter_content(CHUNK_SIZE):
      if chunk:
        progress_bar.update(len(chunk))
        f.write(chunk)
  progress_bar.close()
  if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
    print("ERROR, something went wrong")
  else:
    print("\nDataset file successfully downloaded into path: " + destination)
    if (format == "zip"):
      print("Downloaded file is a zip file. Extracting zip file..")
      os.makedirs(os.path.join(os.path.dirname(destination), name))
      destination_after_extraction = os.path.join(os.path.dirname(destination), name)
      with zipfile.ZipFile(destination, 'r') as zip_ref:
        zip_ref.extractall(os.path.join(os.path.dirname(destination), name))
      os.remove(destination)
      print("Successfully extracted downloaded file into path: " + destination_after_extraction)
      return destination_after_extraction

    return destination
  

def download_cmtt_datasets(name_list):
  """
    Downloads an inbuilt cmtt dataset present in data.json into the user profile directory
    :param name_list: list of cmtt datasets to be downloaded
    :type name_list: list
  """

  if(len(name_list) == 0):
    print("Empty list provided")
    return

  path = os.path.dirname(os.path.realpath(__file__))
  f = open(os.path.join(path, "data.json"))
  data = json.load(f)

  flag = 0

  path_lists = []
  for name in name_list:
    for i in data['datasets']:
      if i['name'] == name:
        url = i['url']
        file_id = i['id']
        source = i['source']
        format = i['format']
        language = i['language']
        flag = 1
        break
    if(flag == 0):
      print("No dataset with the name {} exists".format(name))
      continue
    else:
      flag = 0

    user_root = os.path.expanduser("~")
    newpath = os.path.join(user_root, "cmtt")

    if not os.path.exists(newpath):
      os.makedirs(newpath)
    
    if not os.path.exists(os.path.join(newpath, language)):
      os.makedirs(os.path.join(newpath, language))

    newpath  = os.path.join(newpath, language)
    if os.path.exists(os.path.join(newpath, name+"."+format)) or os.path.isdir(os.path.join(newpath, name)):
      print("Dataset " + name + " already exists at path: "  + newpath)
      if format == "zip":
        path = os.path.join(newpath, name)
      else:
        path = os.path.join(newpath, name+"."+format)
      path_lists.append(path)
    else:
      print("Dataset " + name + " download starting...")
      try:
        if source == "gdrive":
          path = download_file_from_google_drive(file_id, os.path.join(newpath, name+"."+format), name, format)
        else:
          path = download_file(url, os.path.join(newpath, name+"."+format), name, format)
        path_lists.append(path)
      except:
        print("Download failed while downloading " + name)

  f.close()
  return path_lists
            

def download_dataset_url(url, fileName="defaultFileName"):
  """
    Downloads a dataset from a url into 'C:\cmtt'
    :param url: the source url of the dataset
    :type url: str
    :param destination: the filename of the dataset in destination after download
    :type destination: str
  """

  url_parts = url.split(".")
  format = url_parts[-1]
  if format == "gz":
    format = url_parts[-2]

  # newpath = r'C:\cmtt'
  newpath = os.path.join(os.getcwd(), "datasets")
  if not os.path.exists(newpath):
    os.makedirs(newpath)
  if os.path.exists(os.path.join(newpath, fileName+"."+format)) or os.path.isdir(os.path.join(newpath, fileName)):
    print("A dataset with filename " + fileName + " already exists at path: "  + newpath)
    if format == "zip":
      path = os.path.join(newpath, fileName)
    else:
      path = os.path.join(newpath, fileName+"."+format)
  else:
    print("Dataset " + fileName + " download starting...")
    try:
      path = download_file(url, os.path.join(newpath, fileName+"."+format), fileName, format)
    except:
      print("Download failed while downloading " + fileName) 
          
  return path