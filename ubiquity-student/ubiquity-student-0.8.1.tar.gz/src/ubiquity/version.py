"""Module for the ubiquity-student version number"""
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

import requests

from .views.utils import LabelEnum, print_message, print_value, ConsoleColor

file_name = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "VERSION")
with open(file_name, "r", encoding="utf-8") as version_file:
    VERSION = version_file.readline().replace(' ', '')


def check_new_version_client(has_color: bool) -> bool:
    """Function checking if the master has a new version of the client

    :param has_color: Whether the message has color or not
    :return: True if the client has a new version, False if not
    """
    gitlab_version_url = "https://gitlab.insa-rouen.fr/cip/ubiquity/-/raw/master/ubiquity-student/src/VERSION"
    try:
        response = requests.get(gitlab_version_url)
        if response.status_code == 200:
            gitlab_version = response.content.decode("utf-8")
            if VERSION != gitlab_version:
                print_message(LabelEnum.NEW_VERSION_AVAILABLE, color=ConsoleColor.WARNING, end=' ')
                print_value(gitlab_version, color=ConsoleColor.WARNING if has_color else None)
                return True
    except requests.exceptions.ConnectionError:
        print_message(LabelEnum.NO_CONNECTION, color=ConsoleColor.ERROR, end=' ')
    return False
