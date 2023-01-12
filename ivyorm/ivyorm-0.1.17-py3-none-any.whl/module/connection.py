from distutils.log import error
import errno
from sre_compile import isstring
import yaml, importlib
from module.connectors import *
import toml
from module.util.console import Color

    
class Connection:

    config_fullpath = "config.toml"
    conn = object
    config = object
    connection_class = object

    def __init__(self):
        config = self._load_config()
        print(config)
        # now lets call a class that matches the config
        if 'environment' not in config['database']:
            raise ValueError(f"{Color.FAIL}Config: error - 'environment' is missing{Color.END}") 
        
        print(f"{Color.OKCYAN}Config: using config setings for {Color.BOLD}'{config['database']['environment']}'{Color.END}")

        try:
            self.connection_class = importlib.import_module(f"module.connectors.{config['database']['environment']}")
        except:
            raise ValueError(f"{Color.FAIL}Connection: could not find a connection module called '{config['database']['environment']}'{Color.END}")
        

        #my_class = locate(f"module.connection.{config['database_env']}")

        self.config = self._parse_config(config)


        
        self.db_env = '' # filed in from config


        
    

    def run(self, command):
        """
        Attempts to run a command against the database

        :param input: the cqlsh result to parse and format
        :return: the result of the command on the shell
        """
        c = self.connection_class.Conn(self.config) 
        
        return c.run(command)

    def _load_config(self):

        result = {}

        print(f"{Color.HEADER}Config: attempting to load config file...'{Color.END}")

        # LOAD the config file
        
        f = toml.load(self.config_fullpath) 

       
        print(f"{Color.OKCYAN}Config: taml file parsed...'{Color.END}")
        return f


    def _parse_config(self, config):
        # future method to make sure certain config keys exist like host and env

        # make sure there's a 'host' in there some where
        if 'host' not in config['database']:
            print(f"{Color.FAIL}Config: no 'host' list found in the config file{Color.END}")
            exit()
        
        host = config['database']['host']

        # ok, so we know it exists, we're going to see if it's a string or a list. If it's a string, convert it to a list with 1 item
        if isstring(host):
            temp_list = []
            temp_list.append(host)

            config['database']['host'] = temp_list
        
        print(f"{Color.OKCYAN}Config: using the following hosts: {config['database']['host']}{Color.END}")
        return config