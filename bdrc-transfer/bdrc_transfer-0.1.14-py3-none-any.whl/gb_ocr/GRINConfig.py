"""
Base class for configuration
"""
import logging
import os
import sys
from configparser import ConfigParser
from pathlib import Path

class BDRCConfigBase:
    def __init__(self, config_file: str):
        self._default_section_name = "default"
        # subclass inits
        self._config_parser: ConfigParser = ConfigParser()
        self._config_parser.read(config_file)

    def test_init(self):
        """Tests for variable setup before action. subclass inits (I hope)"""
        if not self._config_parser:
            raise ValueError

            #

    # --------------------------------------------------------------------------
    def get_value(self, key: str) -> str:
        """
        :param key:
        :return:  either the current section's entry for the key, or the default
        section, if there is none
        """
        self.test_init()
        rs: str = ""
        try:
            rs = self._config_parser[self._default_section_name][key]
        except KeyError:
            pass
        return rs


class GbSftpConfig(BDRCConfigBase):
    """
    Created on 15 Jun 2022

    Wrapper for a dbConfig file whose format is:
    [default]
    port = "value"
    user = "value"
    host = "value"
    key_path = "value"

    [section]
    port = "value"
    user = "value"
    host = "value"
    key_path = "value"
    ...
    Any key not in 'section' can be fetched from the default

    @author: jsk

    """

    # private variables
    _default_section_name = "default"
    _port_key = "port"  # Tip of the hat to Harry Potter
    _user_key = "user"
    _host_key = "host"
    _key_file_key = "keyFile"
    _gpg_passphrase_key = "gpgPass"
    _configFQPath = None
    _configParser = None
    _operationSection = None

    def __init__(self,  config_file_name: str, type_section: str = "default"):
        """
        Google Books SFTP description
        :param type_section: Optional, can set with section property. Only used in testing
        :param config_file_name: initial file - Now mandatory - was optional, but services cant use env vars
        """
        super().__init__(config_file_name)
        self.op_section = type_section


    # --------------------------------------------------------------------------
    def get_value(self, key: str) -> str:
        """
        Overrides base get_value - because the sftp value has different sections
        with the same keys in it.
        :param key:
        :return:  either the current section's entry for the key, or the default
        section, if there is none
        """
        self.test_init()
        rs: str = ""
        try:
            rs = self._config_parser[self.op_section][key]
        except KeyError:
            try:
                rs = self._config_parser[self._default_section_name][key]
            except KeyError:
                pass
        return rs

    @property
    def config_file_name(self):
        """Config file we are parsing"""
        return self._configFQPath

    @config_file_name.setter
    def config_file_name(self, value):
        """Set the name of the gb_Config file"""

        # unset the current
        if value is None:
            self._configFQPath = None
            self._configParser = None
            return

        cfgPath = Path(value)
        if cfgPath.is_file():
            self._configFQPath = str(cfgPath)
            # Rebuild the _parser
            self._parser(self._configFQPath)
        else:
            # On error, keep existing value
            raise FileNotFoundError(str(cfgPath))

    # --------------------------------------------------------------------------

    @property
    def op_section(self):
        """A section in the config file"""
        return self._operationSection

    @op_section.setter
    def op_section(self, value):
        self._operationSection = value

    # --------------------------------------------------------------------------

    @property
    def port(self) -> int:
        """
        host port
        :return: configured port
        """
        _ = self.get_value(self._port_key)
        return -1 if _ == '' else int(_)

    # --------------------------------------------------------------------------

    @property
    def host(self) -> str:
        """
        host name or IP
        :return: name or IP
        """
        return self.get_value(self._host_key)

    # --------------------------------------------------------------------------

    @property
    def user(self) -> str:
        """
        host name or IP
        :return: name or IP
        """
        return self.get_value(self._user_key)

    # --------------------------------------------------------------------------

    @property
    def key_path(self) -> str:
        """
        host name or IP
        :return: name or IP
        """
        return self.get_value(self._key_file_key)

    # --------------------------------------------------------------------------
    @property
    def gpg_passphrase(self) -> str:
        """
        Return a gpg passphrase
        :return:
        """
        return self.get_value(self._gpg_passphrase_key)

    # --------------------------------------------------------------------------

    def _parser(self, file_name):
        """
        Creates a dbConfig _parser from file_name
        """
        self._configParser = ConfigParser()
        self._configParser.read(file_name)

    # --------------------------------------------------------------------------

    # Override
    def __str__(self):
        return f"config_file_name: {self.config_file_name} section:{self.op_section} port:{self.port} " \
               f"host:{self.host} user:{self.user} key:{self.key_path} "


class GRINConfig(BDRCConfigBase):
    _creds = None
    _resources = None
    _cp: ConfigParser
    _gb_config: GbSftpConfig

    @property
    def cfg_grin_base_url(self):
        return self._resources['server']

    @property
    def cfg_db_config(self):
        return Path(os.path.expanduser(self._creds['db_config_path']))

    @property
    def cfg_credentials_path(self):
        return Path(os.path.expanduser(self._creds['creds_path']))

    @property
    def cfg_log_dir(self):
        return Path(os.path.expanduser(self._resources['log_home']))

    @property
    def cfg_log_level(self) -> int:
        return logging.getLevelName(self._resources['log_level'].upper())

    @property
    def cfg_download_dir(self):
        return Path(os.path.expanduser(self._resources['download_target']))

    @property
    def gb_sftp_config(self):
        """
        GB private configuration
        :return:
        """
        return self._gb_sftp_config

    def __init__(self, type_section: str = '', config_path: Path = None):
        """
        Initializes from GRIN configurations
        :param type_section: only needed for FTP uploads - 'content' or 'metadata'
        :param config_path:
        """
        if not config_path:
            gcp = os.getenv("GRIN_CONFIG")
            if not gcp:
                sys.tracebacklimit = 0
                raise ValueError("GRIN_CONFIG must be defined in the environment")
            config_path = os.path.expanduser(gcp)
        super().__init__(str(config_path))

        self._resources = self._config_parser['resources']
        self._creds = self._config_parser['creds']
        creds_file: str = os.path.expanduser(self._creds['gb_sftp_path'])
        self._gb_sftp_config = GbSftpConfig(type_section=type_section, config_file_name=creds_file)
