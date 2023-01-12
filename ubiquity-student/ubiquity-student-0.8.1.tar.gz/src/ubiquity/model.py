"""Module managing the model"""
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

from tkinter import StringVar
from typing import List, Optional


class Model:
    """Class managing the model"""
    def __init__(self, values: List[Optional[str]]):
        self.name = StringVar()
        self.error = StringVar()
        self.server = StringVar()
        self.student_key = StringVar()
        self.group_key = StringVar()
        self.directory = StringVar()
        self._client_version_min = None
        self._set_values(values)

    def _set_values(self, values: List[Optional[str]]) -> None:
        self.server.set(values[0] if values[0] else '')
        self.student_key.set(values[1] if values[1] else '')
        self.group_key.set(values[2] if values[2] else '')
        self.directory.set(values[3] if values[3] else '')

    def has_server(self):
        """Method verifying that there is a value to server

        :return: True if there is a server, False if not
        """
        return self.server.get() != ""

    def has_student_key(self):
        """Method verifying that there is a value to student key

        :return: True if there is a student key, False if not
        """
        return self.student_key.get() != ""

    def has_group_key(self):
        """Method verifying that there is a value to group key

        :return: True if there is a group key, False if not
        """
        return self.group_key.get() != ""

    def has_directory(self):
        """Method verifying that there is a value to directory

        :return: True if there is a directory, False if not
        """
        return self.directory.get() != ""

    @staticmethod
    def has_input_value(input_var: StringVar):
        """Method verifying that there is a value to the input

        :param input_var: The input
        :return: True if there is a a value to the input, False if not
        """
        return input_var.get() != ""

    @property
    def client_version_min(self) -> str:
        """Get the client version min

        :return: The client version min
        """
        return self._client_version_min

    @client_version_min.setter
    def client_version_min(self, value: str) -> None:
        """Set the client version min

        :param value: The new value
        """
        self._client_version_min = value

    def _url_api_server(self) -> str:
        return f'{self.server.get()}/api'

    def url_api_check_version(self) -> str:
        """Method returning the url for the connection verification to the api

        :return: The string url
        """
        return f'{self._url_api_server()}/check/version'

    def url_api_connection_check(self) -> str:
        """Method returning the url for the connection verification to the api

        :return: The string url
        """
        return f'{self._url_api_server()}/check/{self.student_key.get()}/{self.group_key.get()}'

    def url_api_get_student_environment(self) -> str:
        """Method returning the url for get student environment

        :return: The string url
        """
        return f'{self._url_api_server()}/{self.student_key.get()}/{self.group_key.get()}'

    def url_api_restore_student_environment(self) -> str:
        """Method returning the url for get student environment restored

        :return: The string url
        """
        return f'{self._url_api_server()}/restore/{self.student_key.get()}/{self.group_key.get()}'

    def url_api_get_progress(self) -> str:
        """Method returning the url for get the progress

        :return: The string url
        """
        return f'{self._url_api_server()}/progress/{self.student_key.get()}/{self.group_key.get()}'

    def url_api_file_paths(self) -> str:
        """Method returning the url for get path files to follow

        :return: The string url
        """
        return f'{self._url_api_server()}/{self.group_key.get()}'

    def url_api_action_file(self, file_name: str) -> str:
        """Method returning the url for the file's action

        :return: The string url
        """
        if len(file_name) > 0 and file_name[0] == '/':
            file_name = file_name[1:]
        return f'{self._url_api_server()}/{self.student_key.get()}/{self.group_key.get()}/code_file/{file_name}'

    def url_web_view(self) -> str:
        """Method returning the url for the web view

        :return: The string url
        """
        return f'{self.server.get()}/client/{self.student_key.get()}/{self.group_key.get()}'
