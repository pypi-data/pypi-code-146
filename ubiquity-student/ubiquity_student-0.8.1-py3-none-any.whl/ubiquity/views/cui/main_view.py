"""Module managing the console application views"""
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
import signal
import sys

from ..utils import ConsoleColor, is_success_run, get_color_value, get_percent_value,\
    print_message, LabelEnum, print_value
from ...controllers.main_controller import Returns, MainController
from ...model import Model


def _request_value(label_input: LabelEnum, space: int = 0) -> str:
    """Function displaying an input field and requesting value

    :param label_input: The label
    :param space: The number of spaces
    :return: The input value
    """
    print(label_input.value.rjust(space) + " :", end=' ')
    return input()


def _input_value(label_input: LabelEnum, value: str, space: int = 0) -> None:
    """Function displaying an input field

    :param label_input: The label
    :param value: The value
    :param space: The number of spaces
    """
    print(label_input.value.rjust(space) + " : " + value)


def close(*_, **__):
    """Function to close the application"""
    sys.exit(0)


class MainView:
    """Class managing the main view of console user interface"""
    def __init__(self, model: Model, main_controller: MainController, has_form: bool, has_color: bool) -> None:
        super().__init__()
        signal.signal(signal.SIGINT, close)
        self._model: Model = model
        self._base_values = [
            self._model.server.get(),
            self._model.student_key.get(),
            self._model.group_key.get(),
            self._model.directory.get(),
        ]
        self._main_controller: MainController = main_controller
        self._has_color: bool = has_color
        self.has_form: bool = has_form
        self.form_values(self.has_form)
        if not self.submit():
            self.error_values()
            close()

    def _reset_values(self):
        """Method resetting model values"""
        self._model.server.set(self._base_values[0])
        self._model.student_key.set(self._base_values[1])
        self._model.group_key.set(self._base_values[2])
        self._model.directory.set(self._base_values[3])

    def _display_or_request_value(self, label, input_var, spaces_number: int) -> None:
        """Method displaying or requesting a value

        :param label: The label
        :param spaces_number: The number of spaces
        """
        if self._model.has_input_value(input_var):
            _input_value(label, input_var.get(), spaces_number)
        else:
            input_var.set(_request_value(label, spaces_number))

    def request_values(self, has_form: bool) -> None:
        """Method requesting the values

        :param has_form: If there has form or not
        """
        if has_form:
            print_message(LabelEnum.INFORMATION_REQUEST)
        else:
            print_message(LabelEnum.INFORMATION_DISPLAY)
        spaces_number = LabelEnum.spaces_number()

        self._display_or_request_value(LabelEnum.SERVER, self._model.server, spaces_number)
        self._display_or_request_value(LabelEnum.STUDENT_KEY, self._model.student_key, spaces_number)
        self._display_or_request_value(LabelEnum.GROUP_KEY, self._model.group_key, spaces_number)
        self._display_or_request_value(LabelEnum.DIRECTORY, self._model.directory, spaces_number)

    def confirm_values(self) -> bool:
        """Method static requesting confirm values

        :return: True if is confirmed, False if not
        """
        confirm = _request_value(LabelEnum.CONFIRM)
        is_confirm = confirm in ['y', 'Y']
        if is_confirm:
            print_message(LabelEnum.IS_CONFIRM, 1)
        else:
            print_message(LabelEnum.IS_NOT_CONFIRM, 1, ConsoleColor.WARNING if self._has_color else None)
        return is_confirm

    def error_values(self) -> None:
        """Methode displaying the error message"""
        print_value(self._model.error.get(), 1, ConsoleColor.ERROR if self._has_color else None)

    def form_values(self, has_form: bool) -> None:
        """Methode run the form

        :param has_form: If there has form or not
        """
        self.request_values(has_form)
        if has_form and not self.confirm_values():
            self._reset_values()
            self.form_values(has_form)

    @staticmethod
    def choice() -> str:
        """Method requesting the choice

        :return: The input value
        """
        return _request_value(LabelEnum.RESTORE_OR_RESET)

    def cancel_choice(self, request_again: bool) -> None:
        """Methode displaying the cancel message and run the form

        :param request_again: If request the form again or not
        """
        print_message(LabelEnum.CANCEL_CHOICE, 0, ConsoleColor.WARNING if self._has_color else None)
        if request_again:
            self.form_values(request_again)

    def _show_progress(self, progress_dict):
        progress = progress_dict['progress']
        average = progress_dict['average']
        missing_files = progress_dict['missing_files']
        data = progress_dict['data']
        print_message(LabelEnum.PROGRESS_INFORMATION, end=' ')
        print_message(LabelEnum.PROGRESS, end=' ')
        print_value(get_percent_value(progress), color=get_color_value(self._has_color, progress), end=' ; ')
        print_message(LabelEnum.AVERAGE_PROGRESS, end=' ')
        print_value(get_percent_value(average), color=get_color_value(self._has_color, average), end=' ; ')
        if missing_files > 0:
            print_message(LabelEnum.MISSING_FILES, end=' ')
            print_value(missing_files, end=' ; ')
        print_message(LabelEnum.FILES, enter=1, start=' '*3, end=' ')
        file_names = list(dict.fromkeys([code_block['file_name'] for code_block in data]))
        print_value(len(file_names))
        for file_name in file_names:
            print_value(file_name, start=' '*6, end=' :\n')
            code_blocks = [code_block for code_block in data if code_block['file_name'] == file_name]
            max_len_code_block_name = len(max([code_block['id_block'] for code_block in code_blocks], key=len))
            for code_block in code_blocks:
                code_block_progress = code_block['progress']
                code_block_average = code_block['average']
                print_value(code_block['id_block'], start=' '*9,
                            end=' '*(max_len_code_block_name-len(code_block['id_block'])) + " : ")
                print_message(LabelEnum.PROGRESS, end=' ')
                print_value(get_percent_value(code_block_progress),
                            color=get_color_value(self._has_color, code_block_progress), end=' ; ')
                print_message(LabelEnum.AVERAGE, end=' ')
                print_value(get_percent_value(code_block_average),
                            color=get_color_value(self._has_color, code_block_average), end=' ; ')
                print()
        print()

    def submit(self) -> bool:
        """Method of action on the validation

        return True if submit is ok, False if not
        """
        response = self._main_controller.submit(self._has_color)
        if response == Returns.CHOICE:
            choice = self.choice()
            if choice == '1':
                self._main_controller.extract_restored_zip()
                response = Returns.OK
            elif choice == '2':
                self._main_controller.extract_zip(self._has_color)
                response = Returns.OK
            else:
                self.cancel_choice(self.has_form)
        if response == Returns.OK:
            is_success_run(self._has_color)
            self._main_controller.run(self._show_progress)
            return True
        return False
