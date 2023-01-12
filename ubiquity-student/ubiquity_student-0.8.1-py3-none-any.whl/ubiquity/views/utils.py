"""Module utils view"""
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
import gettext
import os.path
from enum import Enum, unique
from typing import List, Union, Optional, Any

locale = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "locale")
gettext.bindtextdomain('ubiquity-student', locale)
gettext.textdomain('ubiquity-student')
_ = gettext.gettext


class LabelEnum(Enum):
    """Class Enum for label"""
    SERVER = _('Server')
    STUDENT_KEY = _('Student key')
    GROUP_KEY = _('Group key')
    DIRECTORY = _('Directory')
    INFORMATION_REQUEST = _("Please enter the following information:")
    INFORMATION_DISPLAY = _("Information:")
    CONFIRM = _("Do you confirm the information entered? (y/n)")
    IS_CONFIRM = _("You have confirmed your information entered!")
    IS_NOT_CONFIRM = _("You have not confirmed your information entered...")
    RESTORE_OR_RESET = _("Restore(1) or reset(2)?")
    CANCEL_CHOICE = _("No choice...")
    IS_RUN = _("You are now working on this practical work...")
    STUDENT_ENVIRONMENT_RECOVERED = _('The zip file of the student environment has been recovered')
    EXTRACT_ZIP_COMPLETED = _('Extraction of the zip file completed')
    DIRECTORY_CHANGED = _('The working directory has been changed')
    CHOICE = _("Choice")
    NEW = _("New")
    PREFERENCE = _('Preference')
    OPEN = _("Open")
    RECENTLY_OPEN = _("Recently open")
    SEARCH = _("search")
    ACCESS_GROUP = _("Access to the group")
    WARNING = _("Warning")
    RESTORE = _('Restore')
    RESET = _('Reset')
    CANCEL = _('Cancel')
    DELETE = _('Delete')
    ABOUT = _("About")
    VERSION = _("Version:")
    LICENSE = _("License:")
    PROGRESS = _('Progress:')
    AVERAGE = _('Average:')
    AVERAGE_PROGRESS = _('Average progress:')
    MISSING_FILES = _('Missing files:')
    PROGRESS_INFORMATION = _('Progress information:')
    FILES = _('Files:')
    NEW_VERSION_AVAILABLE = _('New version of Ubiquity-student available:')
    WARNING_FILE_EXISTS = _('Warning: File already exists')
    EXTRACT_RESTORED_FILE = _('A file has been restored:')
    RESTORING = _('Restoration of the practical work...')
    NO_CONNECTION = _('No internet connection')
    NO_PRACTICAL_WORK = _('No practical work in progress')
    OPEN_WEB_BROWSER = _('See my progress in the web browser')
    RESTORE_FINISHED = _("The files have been restored")
    DELETE_YES_NO = _("Are you sure you want to delete '%(num)s- %(name)s' ?")
    APPLY = _("Apply")
    THEME = _("Theme")

    @classmethod
    def label_form_list(cls) -> List[str]:
        """Method returning the list of labels of the input fields for the information

        :return: The list of labels
        """
        return [cls.SERVER.value, cls.STUDENT_KEY.value, cls.GROUP_KEY.value, cls.DIRECTORY.value]

    @classmethod
    def spaces_number(cls) -> int:
        """Method returning the number of spaces for labels of the input fields for the information

        :return The number of spaces
        """
        return len(max(cls.label_form_list(), key=len)) + 3


@unique
class ErrorMessage(Enum):
    """Enum class for errors"""
    INVALID_KEYS = _('ERROR: The keys are invalid')
    CONNECTION_FAILED = _('ERROR: Failed to establish the connection')
    DIRECTORY_DOES_NOT_EXIST = _('ERROR: The directory does not exist')
    EMPTY_FIELD = _('ERROR: There are empty input fields')
    CONFIG_DELETED = _('ERROR: The group no longer exists')
    VERSION = _('ERROR: The client version is not valid')


class ConsoleColor(Enum):
    """Class console color"""
    SUCCESS = '\033[92m'  # GREEN
    WARNING = '\033[93m'  # YELLOW
    ERROR = '\033[91m'  # RED
    RESET = '\033[0m'  # RESET COLOR


def print_message(label: Union[LabelEnum, ErrorMessage], enter: int = 0, color: Optional[ConsoleColor] = None,
                  start: Optional[str] = None, end: Optional[str] = None) -> None:
    """Function displaying a message

    :param label: The label
    :param enter: Enter number
    :param color: The color
    :param start: The start print
    :param end: The end print
    """
    print_value(label.value, enter, color, start, end)


def print_value(value: Any, enter: int = 0, color: Optional[ConsoleColor] = None,
                start: Optional[str] = None, end: Optional[str] = None) -> None:
    """Function displaying a value

    :param value: The value
    :param enter: Enter number
    :param color: The color
    :param start: The start print
    :param end: The end print
    """
    print(f'{color.value if color else ""}' + '\n' * enter + f'{start if start else ""}' + str(value) +
          f'{ConsoleColor.RESET.value if color else ""}', end=end)


def get_color_value(has_color: bool, value: Union[int, float]):
    """Function returning the value color

    :param has_color: If the value has color or not
    :param value: The value
    :return: The color
    """
    if not has_color:
        return ConsoleColor.RESET
    if isinstance(value, str):
        return ConsoleColor.ERROR
    if value < 33.33:
        return ConsoleColor.ERROR
    if value < 66.66:
        return ConsoleColor.WARNING
    return ConsoleColor.SUCCESS


def get_percent_value(value: Union[str, int, float]):
    """Function returning the percentage value

    :param value: The value
    :return: The percentage value
    """
    if isinstance(value, str):
        return value
    return f"{value:6.2f}%"


def is_success_run(has_color) -> None:
    """Methode displaying the run message

    :param has_color: If the message has color or not
    """
    print_message(LabelEnum.IS_RUN, 1, ConsoleColor.SUCCESS if has_color else None)
