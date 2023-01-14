import os
from genesys.app.services import svn_service

def write_config(file_directory, config_parser):
    '''
        write data from a configuration parser
        to file
    '''
    with open(file_directory, 'w') as f:
        config_parser.write(f)

def load_config(file_directory, config_parser):
    '''
        load data from a configuration file 
        into a configuration parser instance
    '''
    with open(file_directory, 'r') as f:
        data = f.read()
    config_parser.read_string(data)