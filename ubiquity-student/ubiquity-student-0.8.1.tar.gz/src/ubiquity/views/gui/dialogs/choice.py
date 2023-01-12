"""Module managing the choice dialog"""
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
from tkinter.constants import EW

from .base import BaseDialog
from ...utils import LabelEnum


class ChoiceDialog(BaseDialog):
    """Class for the choice dialog"""
    def __init__(self, parent):
        self.choice = None
        super().__init__(parent, LabelEnum.CHOICE.value)

    def _event_setup(self):
        pass

    def _ui_setup(self):
        mainframe = ttk.Frame(self, padding="3 3 12 12")
        mainframe.pack()
        self.resizable(False, False)

        # Create buttons
        ttk.Button(mainframe, text=LabelEnum.RESTORE.value, command=self.restore).grid(column=0, row=0, sticky=EW)
        ttk.Button(mainframe, text=LabelEnum.RESET.value, command=self.reinit).grid(column=1, row=0, sticky=EW)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def restore(self):
        """Method to choice restore and quit the dialog"""
        self.choice = 1
        self.dismiss()

    def reinit(self):
        """Method to choice reinit and quit the dialog"""
        self.choice = 2
        self.dismiss()
