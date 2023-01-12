"""Module managing the worker"""
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
import time
from enum import unique, IntEnum
from json import loads
from os import stat
from os.path import isfile, join
from threading import Thread
from typing import List

import requests


@unique
class StatusCode(IntEnum):
    """Enum class for status codes"""
    OK = 200
    CREATED = 201


def get_current_time() -> str:
    """Function returning the current time

    :return: The current time
    """
    return time.strftime("%H:%M:%S", time.localtime())


def time_updated_file(file_path):
    """Function returning the time of the updated file

    :param file_path: The file path
    :return: The time of the updated file
    """
    return stat(file_path)[8]


def file_is_updated(file_path, old_time):
    """Function verifying the file is updated

    :param file_path: The file path
    :param old_time: The old time of the updated file
    :return: True if the times is different, False if not
    """
    return old_time != time_updated_file(file_path)


class Worker:
    """Class managing the worker"""
    def __init__(self, model, has_gui, fn_display=None):
        self._model = model
        self._has_gui = has_gui
        self.running = False
        if self._has_gui:
            self._thread = Thread(target=self._worker)
        else:
            self.fn_display = fn_display
        self._files_watching = {}
        self._followed_files = self._get_files_to_follow()
        self._init_files()
        if not self._has_gui:
            self._get_progress()

    def _init_files(self):
        """Method initializing the files to follow"""
        for file_path in self._followed_files:
            if isfile(file_path):
                self._post(file_path)
            else:
                self._delete(file_path)

    def run(self):
        """Method running the worker"""
        self.running = True
        if self._has_gui:
            self._thread.start()
        else:
            self._worker()

    def stop(self):
        """Method stopping the worker"""
        if self.running:
            self.running = False
            if self._has_gui:
                self._thread.join()

    def _worker(self):
        """Method for the worker"""
        while self.running:
            files_path_watching = self._files_watching.copy().keys()
            self._post_or_delete_files_watching(files_path_watching)
            files_path_not_watching = [file_path for file_path in self._followed_files
                                       if file_path not in files_path_watching]
            self._post_new_files(files_path_not_watching)
            time.sleep(0.5)

    def _post_or_delete_files_watching(self, files_path):
        """Method for the files watching

        :param files_path: The files path
        """
        for file_path in files_path:
            if not isfile(file_path):
                self._delete(file_path)
            elif file_is_updated(file_path, self._files_watching[file_path]):
                self._post(file_path)

    def _post_new_files(self, files_path):
        """Method for the new files to watch

        :param files_path: The files path
        """
        for file_path in files_path:
            if isfile(file_path):
                self._post(file_path)

    def _post(self, file_path) -> None:
        try:
            with open(file_path, "r", encoding='utf8') as file:
                data = {'code': file.read()}
            file_name = file_path[len(self._model.directory.get()):]
            response = requests.post(self._model.url_api_action_file(file_name), data=data)
            if response.status_code in [StatusCode.OK, StatusCode.CREATED]:
                self._files_watching[file_path] = time_updated_file(file_path)
                print(f'File {file_path} {"created" if response.status_code == StatusCode.CREATED else "updated" } '
                      f'successfully at {get_current_time()}')
                if not self._has_gui and self.running:
                    self._get_progress()
        except UnicodeDecodeError:
            pass

    def _delete(self, file_path) -> None:
        file_name = file_path[len(self._model.directory.get()):]
        response = requests.delete(self._model.url_api_action_file(file_name))
        if response.status_code == StatusCode.OK:
            try:
                self._files_watching.pop(file_path)
            except KeyError:
                pass
            print(f'File {file_path} deleted successfully at {get_current_time()}')
            if not self._has_gui and self.running:
                self._get_progress()

    def _get_files_to_follow(self) -> List[str]:
        """Method getting the server file paths

        :return: The list of file paths
        """
        response = requests.get(self._model.url_api_file_paths())
        content = loads(response.content)
        return [join(self._model.directory.get(), file['file_path']) for file in content]

    def _get_progress(self) -> None:
        """Method getting the student progress"""
        response = requests.get(self._model.url_api_get_progress())
        self.fn_display(loads(response.content))
