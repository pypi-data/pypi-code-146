"""Module managing the configurations"""
#      ubiquity
#      Copyright (C) 2022  INSA Rouen Normandie - CIP
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.
import datetime
from json import dumps, load, JSONDecodeError
from os.path import join, expanduser, isfile
from typing import List, Optional

from ..model import Model
from ..views.gui.themes import ThemeRegistry
from ..views.gui.themes.sun_valley_light import SunValleyLightTheme


def _get_config_file(config_file_name: str) -> str:
    """Function returning the config file path

    :param config_file_name: The config file name
    :return: The config file path
    """
    return join(expanduser("~"), config_file_name)


def _get_key(model: Model) -> str:
    """Function returning the config key

    :param model: The model
    :return: the config key
    """
    return f'{model.group_key.get()}_{model.student_key.get()}'


class Config:
    """Class managing the configurations"""
    _CONFIG_FILE_NAME = '.ubiquity'
    HISTORY = 'history'
    THEME = 'theme'
    DEFAULT = 'default'
    NAME = 'name'
    DATE = 'date'
    SERVER = 'server'
    STUDENT_KEY = 'student_key'
    GROUP_KEY = 'group_key'
    DIRECTORY = 'directory'

    def __init__(self) -> None:
        self.path_config_file = _get_config_file(Config._CONFIG_FILE_NAME)
        self._default_config = {Config.THEME: SunValleyLightTheme.theme_id(), Config.HISTORY: {}}
        if self._check_has_not_config():
            self._write_config_file(self._default_config)
        self.configs = self._read_config_file()

    def _check_has_not_config(self) -> bool:
        """Method checking if the config file not exist

        :return: True if the config file not exist, False if exist
        """
        return not isfile(self.path_config_file)

    def _read_config_file(self) -> dict:
        """Method returning the config file content

        :return: The config file content
        """
        with open(self.path_config_file, encoding="utf-8") as config_file:
            try:
                configs = load(config_file)
                if Config.HISTORY not in configs:
                    configs = self._default_config.copy()
            except JSONDecodeError:
                configs = self._default_config.copy()
        config_file.close()
        return configs

    def _get_history(self) -> dict:
        try:
            return self.configs[Config.HISTORY]
        except KeyError:
            return self._default_config.copy()[Config.HISTORY]

    def _set_default_config(self, server: str, student_key: str) -> None:
        """Method setting the default config

        :param server: The server url
        :param student_key: The student key
        """
        history = self._get_history()
        history[Config.DEFAULT] = {}
        history[Config.DEFAULT][Config.SERVER] = server
        history[Config.DEFAULT][Config.STUDENT_KEY] = student_key

    def add_config(self, model: Model) -> None:
        """Method adding a config; Or updating if exist

        :param model: The model
        """
        self._set_default_config(model.server.get(), model.student_key.get())
        key = _get_key(model)
        history = self._get_history()
        history[key] = {}
        history[key][Config.NAME] = model.name.get()
        history[key][Config.DATE] = datetime.datetime.now().strftime("%d/%m/%Y")
        history[key][Config.SERVER] = model.server.get()
        history[key][Config.STUDENT_KEY] = model.student_key.get()
        history[key][Config.GROUP_KEY] = model.group_key.get()
        history[key][Config.DIRECTORY] = model.directory.get()
        self._write_config_file(self.configs)

    def remove_config(self, model: Model) -> None:
        """Method removing a config by a group key

        :param model: The model
        """
        self._get_history().pop(_get_key(model))
        self._write_config_file(self.configs)

    def check_is_config(self, model: Model) -> bool:
        """Method checking if config exist

        :param model: The model
        :return: True if the values exist in the config file. False if not
        """
        history = self._get_history()
        key = _get_key(model)
        if key in history:
            config = history[key]
            if config[Config.SERVER] == model.server.get() and config[Config.STUDENT_KEY] == model.student_key.get() \
                    and config[Config.DIRECTORY] == model.directory.get():
                return True
        return False

    def check_directory(self, model: Model) -> bool:
        """Method checking if directory exist and if is in the config file

        :param model: The model
        :return: True if the directory is valid. False if not
        """
        history = self._get_history()
        key = _get_key(model)
        if key in history:
            return history[key][Config.DIRECTORY] == model.directory.get()
        return False

    def set_theme(self, theme):
        """Method to set up the theme and save in the config file

        :param theme: The new theme
        """
        self.configs[Config.THEME] = theme
        self._write_config_file(self.configs)

    def init_theme(self):
        """Method to init the theme"""
        theme = ThemeRegistry().get_theme_by_id(self.configs[Config.THEME])
        if theme is not None:
            theme.use_theme(self)

    def _write_config_file(self, configs: dict) -> None:
        """Method writing the config file

        :param configs: The configs
        """
        with open(self.path_config_file, 'w+', encoding='utf8') as config_file:
            config_file.write(dumps(configs))
        config_file.close()

    def list_config(self, values: List[Optional[str]]) -> dict:
        """Function returning the list of configs

        :param values: The values list
        :return: The list of configs
        """
        configs = self._get_history().copy()
        if Config.DEFAULT in configs:
            configs.pop(Config.DEFAULT)
        servers = {}
        for number, key in enumerate(configs, 1):
            config_values = configs[key]
            config_server = config_values[self.SERVER]
            is_server_in_list = not values[0] or values[0] == config_server
            is_student_key_in_list = not values[1] or values[1] == config_values[self.STUDENT_KEY]
            is_group_key_in_list = not values[2] or values[2] == config_values[self.GROUP_KEY]
            is_directory_in_list = not values[3] or values[3] == config_values[self.DIRECTORY]
            if is_server_in_list and is_student_key_in_list and is_group_key_in_list and is_directory_in_list:
                if config_server not in servers:
                    servers[config_server] = {}
                if config_values[self.STUDENT_KEY] not in servers[config_server]:
                    servers[config_server][config_values[self.STUDENT_KEY]] = {}
                servers[config_server][config_values[self.STUDENT_KEY]][config_values[self.GROUP_KEY]] = {
                    'id': str(number),
                    'name': config_values[self.NAME],
                    'date': config_values[self.DATE] if self.DATE in config_values else None,
                    'directory': config_values[self.DIRECTORY]
                }
        return servers
