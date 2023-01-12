"""Module managing the main window"""
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

from tkinter import ttk
from tkinter.constants import W, EW
import webbrowser

from .dialogs import ChoiceDialog
from ..utils import is_success_run, LabelEnum
from ...model import Model
from ...controllers.main_controller import MainController, Returns


class MainView(ttk.Frame):
    """Class managing the main view of graphic user interface"""
    def __init__(self, parent, has_form, has_color):
        super().__init__()
        self.menu_bar = parent.menu_bar
        self.model: Model = parent.model
        self.main_controller: MainController = parent.controller
        self._has_form: bool = has_form
        self._has_color: bool = has_color
        self.mainframe = ttk.Frame()
        self.mainframe.pack()
        if has_form:
            self.main_controller.init_values()
            self._ui_setup()
        else:
            self.submit()

    def _ui_setup(self):
        self._clear()
        ttk.Label(self.mainframe, text=LabelEnum.NO_PRACTICAL_WORK.value).grid(column=0, row=0, pady=20)

    def submit(self):
        """Method to submit values and run worker if the values are valid

        :return: True if running, False if not
        """
        response = self.main_controller.submit(self._has_color)
        if response == Returns.CHOICE:
            choice_dialog = ChoiceDialog(self)
            if choice_dialog.choice == 1:
                self.main_controller.extract_restored_zip()
                response = Returns.OK
            elif choice_dialog.choice == 2:
                self.main_controller.extract_zip(self._has_color)
                response = Returns.OK
            else:
                self.menu_bar.update_menu(False)
                self._ui_setup()
        if response == Returns.OK:
            is_success_run(self._has_color)
            self.run()
            return True
        return False

    def run(self):
        """Method run and open a web browser"""
        self._clear()
        self.main_controller.run()
        ttk.Label(self.mainframe, textvariable=self.model.server).grid(column=2, row=1, sticky=W, padx=5, pady=(15, 5))
        ttk.Label(self.mainframe, textvariable=self.model.student_key).grid(column=2, row=2, sticky=W, padx=5, pady=5)
        ttk.Label(self.mainframe, textvariable=self.model.group_key).grid(column=2, row=3, sticky=W, padx=5, pady=5)
        ttk.Label(self.mainframe, textvariable=self.model.directory).grid(column=2, row=4, sticky=W, padx=5, pady=5)
        ttk.Label(self.mainframe, text=LabelEnum.SERVER.value).grid(column=1, row=1, sticky=W, padx=5, pady=(15, 5))
        ttk.Label(self.mainframe, text=LabelEnum.STUDENT_KEY.value).grid(column=1, row=2, sticky=W, padx=5, pady=5)
        ttk.Label(self.mainframe, text=LabelEnum.GROUP_KEY.value).grid(column=1, row=3, sticky=W, padx=5, pady=5)
        ttk.Label(self.mainframe, text=LabelEnum.DIRECTORY.value).grid(column=1, row=4, sticky=W, padx=5, pady=5)
        ttk.Button(self.mainframe, text=LabelEnum.OPEN_WEB_BROWSER.value, command=self._open_web_browser)\
            .grid(column=1, columnspan=2, row=5, sticky=EW, pady=5)

    def stop(self):
        """Method stop"""
        self.main_controller.stop()
        self._ui_setup()
        self.model.server.set("")
        self.model.student_key.set("")
        self.model.group_key.set("")
        self.model.directory.set("")

    def _open_web_browser(self):
        """Method opening a web browser"""
        webbrowser.open(self.model.url_web_view())

    def _clear(self):
        """Method to clear the view"""
        for widget in self.mainframe.winfo_children():
            widget.destroy()
