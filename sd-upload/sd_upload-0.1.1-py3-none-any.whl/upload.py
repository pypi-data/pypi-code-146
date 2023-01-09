#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import validators
import json
import zipfile
import argparse

#********** Credentials to login **********
robin_email = "YOUR EMAIL"
robin_password = "YOUR PASSWORD"

# ********** API URL **********
api_url = "https://URL" #production

# ********** Global variables **********
bearer_token = ''

def validate_radar_type(radarType):
    radarTypearray = ["elvira", "iris", "max", "3dfixed"]
    if validators.length(radarType, min=1, max=50) == False:
        print("Radar type is not valid: " + radarType)
        exit()
        #check if radar type is in the array
    if radarType not in radarTypearray:
            print("Radar type is not valid: " + radarType)
            exit()
    else:
        print("Radar type is valid: " + radarType)
        return radarType

def validate_version_name(version_name):
    if validators.length(version_name, min=1, max=20) == False:
        print("Version name is not valid: " + version_name)
        exit()
    else:
        print("Version name is valid: " + version_name)
        return version_name

def get_bearer_token():
    headers = {
        'Content-Type': 'application/json',
    }

    data = '{"email": "' + robin_email + '", "password": "' + robin_password + '"}'
    response = requests.post(api_url + '/api/auth/login', headers=headers, data=data)

    bearer_token = response.json()['token']
    return bearer_token

def create_zip(zip_name, folder_name):
    #check if folder exists
    if os.path.isdir(folder_name):
        print("Folder exists: " + folder_name)
    else:
        return "Folder not exist: " + folder_name
    zipf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(folder_name):
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close()

#remove zip file if exists
def remove_zip(zip_name):
    if os.path.isfile(zip_name):
        os.remove(zip_name)
        print("ZIP file removed: " + zip_name)
    else:
        return "ZIP not exist: " + zip_name

def push_software(fpath):
    headers = {
        'Authorization': 'Bearer ' + bearer_token,
    }
    if not bearer_token:
        return "Bearer token is empty"
    else:
        print('bearer_token: ', bearer_token)

    # check if can open file path
    if os.path.isfile(zipped_file_path):
        print("ZIP file exists: " + zipped_file_path)
    else:
        return "ZIP not exist: " + zipped_file_path
        
    files = {
        'file': (fpath, open(fpath, 'rb'))
    }

    values = {
        'destination': json.dumps(radarType),
        'versionName': json.dumps(version_name)
    }
    
    print('Uploading software...')

    response = requests.post(api_url+'/api/softwares/softwarefiles', headers=headers, data=values, files=files)
    return response.json()

if __name__ == '__main__':
    # usage: python ./upload.py --type='type' --version='2.2.x'
    print("--- Start ---")

    parser = argparse.ArgumentParser(description='argument parses for upload script.')
    parser.add_argument("--type", type=str, help="radar type")
    parser.add_argument("--version", type=str, help="version name")
    args = parser.parse_args()

    radarType = args.type
    version_name = args.version

    print("given type: ", radarType)
    print("given version_name: ", version_name)

    version_dir_to_upload= os.path.dirname(os.path.realpath(__file__))+"/"+version_name
    zipped_file_path = os.path.dirname(os.path.realpath(__file__))+"/"+version_name+".zip"

    validate_radar_type(radarType)
    validate_version_name(version_name)
    create_zip(zipped_file_path, version_name)
    bearer_token = get_bearer_token()
    print(push_software(zipped_file_path))
    remove_zip(zipped_file_path)
    print("--- End ---")