"""Module managing the base dialog"""
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

import abc
from tkinter import Toplevel


class BaseDialog(Toplevel, abc.ABC):
    """Abstract dialog class"""
    def __init__(self, parent, title):
        super().__init__(parent)
        self.title = title
        self.is_valid = False
        self._model = parent.model
        self._setup_dialog(parent)

    def _setup_dialog(self, parent):
        """Method for setting up the dialog

        :param parent: The parent view
        """
        self._ui_setup()
        self._event_setup()
        self._config_setup(parent)

    def _config_setup(self, parent):
        """Method for configuring the dialog

        :param parent: The parent view
        """
        self.wm_title(self.title)
        self.protocol("WM_DELETE_WINDOW", self.dismiss)
        self.transient(parent)
        self.wait_visibility()
        self.grab_set()
        self.wait_window()

    @abc.abstractmethod
    def _event_setup(self):
        """Method for setting up the dialog events"""

    @abc.abstractmethod
    def _ui_setup(self):
        """Method for setting up the dialog user interface"""

    def dismiss(self):
        """Method closing the dialog"""
        self.grab_release()
        self.destroy()
