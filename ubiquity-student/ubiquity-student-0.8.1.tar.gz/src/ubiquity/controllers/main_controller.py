"""Module managing the application controller"""
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
import os.path
from enum import unique, Enum, auto
from io import BytesIO
from json import loads
from json.decoder import JSONDecodeError
from typing import Optional
from zipfile import ZipFile

import requests

from .config_file import Config
from .worker import Worker, StatusCode
from .. import __version__
from ..model import Model
from ..views.utils import print_message, LabelEnum, ErrorMessage, print_value, ConsoleColor


@unique
class Returns(Enum):
    """Enum class for returns on submit method"""
    CHOICE = auto()
    OK = auto()
    ERROR = auto()


class MainController:
    """Class managing the main controller"""
    def __init__(self, config: Config, model: Model, has_gui) -> None:
        super().__init__()
        self._model = model
        self.worker = None
        self.config = config
        self.has_gui = has_gui
        self.is_new_project = False

    def init_values(self) -> None:
        """Method initializing the state values"""
        if Config.DEFAULT in self.config.configs[Config.HISTORY] and True not in [self._model.has_server(),
                                                                                  self._model.has_student_key(),
                                                                                  self._model.has_group_key(),
                                                                                  self._model.has_directory()]:
            self._model.server.set(self.config.configs[Config.HISTORY][Config.DEFAULT][Config.SERVER])
            self._model.student_key.set(self.config.configs[Config.HISTORY][Config.DEFAULT][Config.STUDENT_KEY])

    def _check_values(self) -> Optional[ErrorMessage]:
        """Method verifying if the state values are valid

        :return: True if the values are valid, False if not
        """
        error = self._check_values_not_empty()
        if error is None:
            error = self._check_connection()
        if error is None:
            error = self._check_directory()
        if isinstance(error, ErrorMessage):
            self._model.error.set(error.value)
            return error
        return None

    def _check_values_not_empty(self) -> Optional[ErrorMessage]:
        """Method verifying if the state values are not empty

        :return: None if the values are valid, Error if not
        """
        if "" in [self._model.server.get(), self._model.student_key.get(),
                  self._model.group_key.get(), self._model.directory.get()]:
            return ErrorMessage.EMPTY_FIELD
        return None

    def _check_version(self) -> Optional[ErrorMessage]:
        """Method verifying if the client version is OK

        :return: None if the client version is OK, Error if not
        """
        response = requests.get(self._model.url_api_check_version())
        try:
            content = loads(response.content)
            self._model.client_version_min = content['version_min']
            if content['version_min'] <= __version__:
                return None
        except JSONDecodeError:
            return None
        return ErrorMessage.VERSION

    def _check_connection(self) -> Optional[ErrorMessage]:
        """Method verifying if the connection is OK

        :return: None if the status code is OK, Error if not
        """
        try:
            response = self._check_version()
            if response:
                return response
            response = requests.get(self._model.url_api_connection_check())
            if response.status_code != StatusCode.OK:
                if self.config.check_is_config(self._model):
                    return ErrorMessage.CONFIG_DELETED
                return ErrorMessage.INVALID_KEYS
            content = loads(response.content)
            self._model.name.set(content['name'])
            self.is_new_project = content['is_new']
        except requests.exceptions.RequestException:
            return ErrorMessage.CONNECTION_FAILED
        return None

    def _check_directory(self) -> Optional[ErrorMessage]:
        """Method verifying if the directory exits

        :return: None if exists, Error if not
        """
        if not os.path.exists(self._model.directory.get()):
            return ErrorMessage.DIRECTORY_DOES_NOT_EXIST
        return None

    def extract_zip(self, has_color: bool = False) -> None:
        """Extract a zip file to the working directory

        :param has_color: True if text has color, False if not
        """
        response = requests.get(self._model.url_api_get_student_environment())
        with ZipFile(BytesIO(response.content)) as zip_file:
            print_message(LabelEnum.STUDENT_ENVIRONMENT_RECOVERED)
            for filename in zip_file.namelist():
                if os.path.exists(os.path.join(self._model.directory.get(), filename)):
                    print_message(LabelEnum.WARNING_FILE_EXISTS,
                                  color=ConsoleColor.WARNING if has_color else None,
                                  end=" ")
                    print_value(filename)
                else:
                    zip_file.extract(filename, self._model.directory.get())
        print_message(LabelEnum.EXTRACT_ZIP_COMPLETED, 1)

    def extract_restored_zip(self) -> None:
        """Extract a restored zip file to the working directory"""
        response = requests.get(self._model.url_api_restore_student_environment())
        print_message(LabelEnum.RESTORING)
        with ZipFile(BytesIO(response.content)) as zip_file:
            print_message(LabelEnum.STUDENT_ENVIRONMENT_RECOVERED)
            for filename in zip_file.namelist():
                if not os.path.exists(os.path.join(self._model.directory.get(), filename)):
                    zip_file.extract(filename, self._model.directory.get())
                    print_message(LabelEnum.EXTRACT_RESTORED_FILE, end=" ")
                    print_value(filename)
        print_message(LabelEnum.EXTRACT_ZIP_COMPLETED, 1)

    def _check_is_new(self) -> bool:
        """Method checking if is a new project

        :return: True if is a new project, False if not
        """
        return not self.config.check_is_config(self._model)

    def _add_config(self) -> None:
        """Method adding a config"""
        self.config.add_config(self._model)

    def update_with_config(self, config: dict) -> None:
        """Method updating the model with the config values

        :param config: The config
        """
        self._model.server.set(config[Config.SERVER])
        self._model.student_key.set(config[Config.STUDENT_KEY])
        self._model.group_key.set(config[Config.GROUP_KEY])
        self._model.directory.set(config[Config.DIRECTORY])
        self._model.error.set('')

    def run(self, fn_display=None) -> None:
        """Method running the worker and add values in the config file"""
        self._add_config()
        if self.has_gui:
            self.worker = Worker(self._model, self.has_gui)
        else:
            self.worker = Worker(self._model, self.has_gui, fn_display)
        self.worker.run()

    def stop(self) -> None:
        """Method stopping the worker"""
        self.worker.stop()

    def submit(self, has_color: bool = False) -> Returns:
        """Method verifying the values and run the worker

        :param has_color: True if text has color, False if not
        :return: The status of the return on the form validation
        """
        error = self._check_values()
        if not isinstance(error, ErrorMessage):
            if self.is_new_project:
                self.extract_zip(has_color)
            elif not self.config.check_directory(self._model):
                return Returns.CHOICE
            return Returns.OK
        if error is not ErrorMessage.VERSION and error is not ErrorMessage.CONNECTION_FAILED and \
                self.config.check_is_config(self._model):
            self.config.remove_config(self._model)
        return Returns.ERROR
