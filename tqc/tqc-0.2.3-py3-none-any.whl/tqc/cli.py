import os
import json
import random
import requests
import sys
import yaml
from colorama import init
from zipfile import ZipFile

DEFAULT_COMPILER = 'https://compile.tinyqueries.com'
POSSIBLE_CONFIG_FILE_NAMES = [
    'tinyqueries.json',
    'tinyqueries.yml',
    'tinyqueries.yaml',
]

def get_api_key():
    key = os.environ.get('TINYQUERIES_API_KEY')
    if key is None:
        raise Exception('No API key found - please add your TinyQueries API key to your ENV variables')
    return key

def read_config():
    for filename in POSSIBLE_CONFIG_FILE_NAMES:
        if os.path.exists(filename):
            fh = open(filename, "r")
            _, file_extension = os.path.splitext(filename)
            if file_extension == '.json':
                config = json.loads(fh.read())
            else:
                config = yaml.load(fh, Loader=yaml.FullLoader)
            if config is None:
                raise Exception('Error decoding config file ' + filename)
            fh.close()
            standardize_config(config)
            config['filename'] = filename
            return config
    raise Exception('No config file found in current folder - Please create a config file tinyqueries.yaml')

def standardize_config(config):
    if not 'project' in config:
        config['project'] = {}
    if not 'label' in config['project']:
        config['project']['label'] = ''
    if not 'compiler' in config:
        config['compiler'] = {}
    if not 'server' in config['compiler']:
        config['compiler']['server'] = DEFAULT_COMPILER
    if not 'version' in config['compiler']:
        config['compiler']['version'] = 'latest'
    if not 'input' in config['compiler']:
        config['compiler']['input'] = 'tinyqueries'

def is_file_to_upload(entry):
    if entry in POSSIBLE_CONFIG_FILE_NAMES:
        return False
    else:
        return True

def add_folder_recursively_to_zip(zip, folder, folder_relative = ''):
    for entry in os.scandir(path=folder):
        if is_file_to_upload(entry):
            path = folder + '/' + entry.name
            if folder_relative == '':
                path_relative = entry.name
            else:
                path_relative = folder_relative + '/' + entry.name
            if entry.is_dir():
                add_folder_recursively_to_zip(zip, path, path_relative)
            else:
                zip.write(path, path_relative)

def send_compile_request(config, api_key):
    if not os.path.exists(config['compiler']['input']):
        raise Exception('Cannot find input folder ' + config['compiler']['input'])
    tag = str(random.randint(1000000000,9999999999))
    zip_filename = 'upload-' + tag + '.zip'
    zip = ZipFile(zip_filename, 'w')
    zip.write(config['filename'])
    add_folder_recursively_to_zip(zip, config['compiler']['input'])
    zip.close()
    print("Uploading zip to compiler..")
    response = requests.post(
        url = config['compiler']['server'],
        headers = {
            'Authorization': 'Bearer ' + api_key
        },
        files = {
            'tq_code': open(zip_filename,'rb')
        }
    )
    os.remove(zip_filename)
    if response.status_code != 200:
        if response.headers.get('content-type') == 'application/json':
            raise Exception(response.json()['error'])
        else:
            raise Exception(response)
    print("Extracting received zip..")
    zip_filename = 'download-' + tag + '.zip'
    fh = open(zip_filename, 'wb')
    fh.write(response.content)
    fh.close()
    zip = ZipFile(zip_filename, 'r')
    zip.extractall()
    zip.close()
    os.remove(zip_filename)

def main():
    try:
        init()
        print('\033[1;33mTiny\033[1;37mQueries\033[0m')
        api_key = get_api_key()
        config = read_config()
        print("- project: " + config['project']['label'])
        print("- server: " + config['compiler']['server'])
        print("- version: " + config['compiler']['version'])
        print("- input folder: " + config['compiler']['input'])
        send_compile_request(config, api_key)
        print('\033[1;37mReady\033[0m')
        exit(0)
    except Exception as err:
        print('\033[1;31m' + str(err) + '\033[0m')
        exit(1)
