"""Module managing the about dialog"""
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
import os
from tkinter import PhotoImage, ttk

from .base import BaseDialog
from ...utils import LabelEnum
from ....version import VERSION


class AboutDialog(BaseDialog):
    """Class for the about dialog"""
    LOGO_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))), "images/ubiquity_icon.png")

    def __init__(self, parent):
        self.photo = PhotoImage(file=AboutDialog.LOGO_PATH)
        super().__init__(parent, LabelEnum.ABOUT.value)

    def _event_setup(self):
        pass

    def _ui_setup(self):
        mainframe = ttk.Frame(self, padding="3 3 12 12")
        mainframe.pack()
        self.resizable(False, False)

        ttk.Label(mainframe, image=self.photo).grid(column=0, row=0, rowspan=3)
        ttk.Label(mainframe, text="Ubiquity Student").grid(column=1, row=0)
        ttk.Label(mainframe, text=f"{LabelEnum.VERSION.value} {VERSION}").grid(column=1, row=1)
        ttk.Label(mainframe, text=f"{LabelEnum.LICENSE.value} Copyright (C) 2022  INSA Rouen Normandie - CIP")\
            .grid(column=1, row=2)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)
