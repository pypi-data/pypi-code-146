"""Module managing the form dialog"""
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

from tkinter import ttk, filedialog
from tkinter.constants import W, EW

from .base import BaseDialog
from ...utils import LabelEnum, ErrorMessage


class FormDialog(BaseDialog):
    """Class for the form dialog"""
    def __init__(self, parent):
        self.parent = parent
        self.parent.model.error.set('')
        super().__init__(parent, LabelEnum.NEW.value)

    def _event_setup(self):
        self.bind("<Return>", self.access)

    def _ui_setup(self):
        mainframe = ttk.Frame(self, padding="3 3 12 12")
        mainframe.pack()
        self.resizable(False, False)

        # Create Entries
        server_entry = ttk.Entry(mainframe, width=50, textvariable=self._model.server)
        server_entry.grid(column=2, row=1, sticky=EW)
        server_entry.focus()
        ttk.Entry(mainframe, textvariable=self._model.student_key).grid(column=2, row=2, sticky=EW)
        ttk.Entry(mainframe, textvariable=self._model.group_key).grid(column=2, row=3, sticky=EW)
        ttk.Entry(mainframe, textvariable=self._model.directory).grid(column=2, row=4, sticky=EW)

        # Create labels
        ttk.Label(mainframe, textvariable=self._model.error, foreground='#F00').grid(column=1, columnspan=3, row=0)
        ttk.Label(mainframe, text=LabelEnum.SERVER.value).grid(column=1, row=1, sticky=W)
        ttk.Label(mainframe, text=LabelEnum.STUDENT_KEY.value).grid(column=1, row=2, sticky=W)
        ttk.Label(mainframe, text=LabelEnum.GROUP_KEY.value).grid(column=1, row=3, sticky=W)
        ttk.Label(mainframe, text=LabelEnum.DIRECTORY.value).grid(column=1, row=4, sticky=W)

        # Create buttons
        ttk.Button(mainframe, text=LabelEnum.SEARCH.value, command=self.search).grid(column=3, row=4, sticky=EW)
        ttk.Button(mainframe, text=LabelEnum.ACCESS_GROUP.value, command=self.access).grid(column=2, row=5, sticky=EW)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def search(self):
        """Method searching a directory"""
        dir_name = filedialog.askdirectory(parent=self)
        if dir_name:
            self._model.directory.set(dir_name)

    def _is_valid(self):
        """Method verifying the form is valid

        :return: True if the values are valid, False if not
        """
        if '' in [self._model.server.get(), self._model.student_key.get(), self._model.group_key.get(),
                  self._model.directory.get()]:
            self._model.error.set(ErrorMessage.EMPTY_FIELD.value)
            return False
        return True

    def access(self, *_):
        """Method accessing and run if the values are valid"""
        self._model.error.set('')
        if self._is_valid():
            self.is_valid = self.parent.submit()
            if self.is_valid:
                self.dismiss()
