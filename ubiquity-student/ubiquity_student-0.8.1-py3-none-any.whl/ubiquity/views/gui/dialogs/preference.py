"""Module managing the preference dialog"""
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

from tkinter import ttk, Listbox
from tkinter.constants import END, LEFT, BOTTOM, BOTH, RIGHT, TOP, CENTER

from .base import BaseDialog
from ..themes import ThemeRegistry
from ...utils import LabelEnum
from ....controllers.config_file import Config


class PreferenceDialog(BaseDialog):
    """Class for the preference dialog"""
    def __init__(self, parent):
        self.parent = parent
        self.mainframe = None
        self.nav = None
        super().__init__(parent, LabelEnum.PREFERENCE.value)

    def _event_setup(self):
        pass

    def _ui_setup(self):
        self.geometry("500x300")
        self._ui_setup_list_choice()
        self._display_theme()
        self._ui_buttons()

    def _ui_buttons(self):
        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(side=BOTTOM, pady=2)
        ttk.Button(bottom_frame, text=LabelEnum.APPLY.value, command=self.mainframe.apply).pack(side=LEFT, padx=3)
        ttk.Button(bottom_frame, text=LabelEnum.CANCEL.value, command=self.dismiss).pack(side=RIGHT, padx=3)

    def _ui_setup_list_choice(self):
        self.nav = Listbox(self)
        self.nav.insert(END, LabelEnum.THEME.value)
        self.nav.select_set(0)
        self.nav.pack(side=LEFT, fill=BOTH)

    def _display_theme(self):
        self._clear()
        self.mainframe = ThemeWidget(self)
        self.mainframe.pack()

    def _clear(self):
        """Method to clear the view"""
        if self.mainframe:
            for widget in self.mainframe.winfo_children():
                widget.destroy()


class ThemeWidget(ttk.Frame):
    """Class widget for the theme preference"""
    def __init__(self, master):
        super().__init__(master, padding="3 3 12 12")
        self.theme_registry = ThemeRegistry()
        self.controller = master.parent.main_controller
        self.combobox = ttk.Combobox(self, state='readonly', values=[name for name in self.theme_registry.themes_names])
        config_theme = self.theme_registry.get_theme_by_id(self.controller.config.configs[Config.THEME])
        if config_theme is not None:
            self.combobox.set(config_theme.theme_name())
        self.ui_setup()

    def ui_setup(self):
        """Method setting up the user interface"""
        ttk.Label(self, text=LabelEnum.THEME.value).pack(side=TOP, anchor=CENTER, pady=(10, 20))
        self.combobox.pack()

    def apply(self):
        """Method applying the theme"""
        self.theme_registry.themes_classes[self.combobox.get()].use_theme(self.controller.config)
