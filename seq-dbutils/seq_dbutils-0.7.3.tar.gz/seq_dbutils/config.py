import logging
import os
import sys
from configparser import ConfigParser

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class Config:
    configParser = ConfigParser()

    @classmethod
    def initialize(cls, config_file_path):
        if not os.path.isfile(config_file_path):
            logging.error(f'Config file {config_file_path} does not exist. Exiting...')
            sys.exit(1)
        cls.configParser.read(config_file_path)

    @classmethod
    def get_section_config(cls, required_section, required_key):
        return cls.configParser.get(required_section, required_key)

    @staticmethod
    def get_db_config(required_section):
        assert required_section
        try:
            logging.info(f"Extracting config for '{required_section}'")
            user = Config.get_section_config(required_section, 'user')
            key = Config.get_section_config(required_section, 'key').encode()
            host = Config.get_section_config(required_section, 'host')
            db = Config.get_section_config(required_section, 'db')
            return user, key, host, db

        except Exception as ex:
            logging.error(str(ex))
            sys.exit(1)
