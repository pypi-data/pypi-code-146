"""Module managing the menu bar"""
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
import webbrowser
from enum import Enum
from tkinter import Menu, messagebox
from tkinter.constants import DISABLED, NORMAL

from .dialogs import AboutDialog, FormDialog, OpenDialog, PreferenceDialog
from ..utils import gettext, LabelEnum

_ = gettext.gettext


class MenuLabel(Enum):
    """Class Enum for menu label"""
    FILE = _('File')
    NEW_FILE_ACTION = _('New...')
    OPEN_FILE_ACTION = _('Recently open...')
    CLOSE_FILE_ACTION = _('Close')
    RESTORE_FILE_ACTION = _('Restore')
    PREFERENCE_FILE_ACTION = _('Preference...')
    EXIT_FILE_ACTION = _('Exit')
    HELP = _('Help')
    HELP_HELP_ACTION = _('Help...')
    ABOUT_HELP_ACTION = _('About...')


class MenuBar(Menu):
    """Class managing the menu bar"""

    def __init__(self, parent, has_form):
        super().__init__(parent)
        self.parent = parent
        self.menu_file = self._menu_file_setup()
        self.menu_help = self._menu_help_setup()
        self.update_menu(not has_form)

    def _menu_file_setup(self):
        """Method setting up the file menu

        :return: The file menu
        """
        menu_file = Menu(self, tearoff=False)
        menu_file.add_command(label=f'  {MenuLabel.NEW_FILE_ACTION.value}', command=self.new_file, underline=2)
        menu_file.add_command(label=f'  {MenuLabel.OPEN_FILE_ACTION.value}', command=self.open_file)
        menu_file.add_command(label=f'  {MenuLabel.RESTORE_FILE_ACTION.value}', command=self.restore_file, underline=2)
        menu_file.add_command(label=f'  {MenuLabel.CLOSE_FILE_ACTION.value}', command=self.close_file)
        menu_file.add_command(label=f'  {MenuLabel.PREFERENCE_FILE_ACTION.value}', command=self.preference_file)
        menu_file.add_command(label=f'  {MenuLabel.EXIT_FILE_ACTION.value}', command=self.exit_file)
        self.add_cascade(menu=menu_file, label=MenuLabel.FILE.value, underline=0)
        return menu_file

    def _menu_help_setup(self):
        """Method setting up the help menu

        :return: The help menu
        """
        menu_help = Menu(self, tearoff=False)
        menu_help.add_command(label=f'  {MenuLabel.HELP_HELP_ACTION.value}', command=self.help_help, underline=2)
        menu_help.add_command(label=f'  {MenuLabel.ABOUT_HELP_ACTION.value}', command=self.about_help, underline=2)
        self.add_cascade(menu=menu_help, label=MenuLabel.HELP.value, underline=0)
        return menu_help

    def update_menu(self, is_opened_file: bool):
        """Method updating the menu

        :param is_opened_file: If a project is opened
        """
        self.menu_file.entryconfigure(f'  {MenuLabel.NEW_FILE_ACTION.value}',
                                      state=DISABLED if is_opened_file else NORMAL)
        self.menu_file.entryconfigure(f'  {MenuLabel.OPEN_FILE_ACTION.value}',
                                      state=DISABLED if is_opened_file else NORMAL)
        self.menu_file.entryconfigure(f'  {MenuLabel.RESTORE_FILE_ACTION.value}',
                                      state=NORMAL if is_opened_file else DISABLED)
        self.menu_file.entryconfigure(f'  {MenuLabel.CLOSE_FILE_ACTION.value}',
                                      state=NORMAL if is_opened_file else DISABLED)

    def new_file(self):
        """Method of the action "new" in file menu"""
        self.update_menu(FormDialog(self.parent.view).is_valid)

    def open_file(self):
        """Method of the action "open" in file menu"""
        self.update_menu(OpenDialog(self.parent.view, self.parent.controller.config).is_valid)

    def restore_file(self):
        """Method of the action "restore" in file menu"""
        self.parent.controller.extract_restored_zip()
        messagebox.showinfo(message=LabelEnum.RESTORE_FINISHED.value)

    def close_file(self):
        """Method of the action "close" in file menu"""
        self.update_menu(False)
        self.parent.view.stop()

    def preference_file(self):
        """Method of the action "close" in file menu"""
        PreferenceDialog(self.parent.view)

    def exit_file(self):
        """Method of the action "exit" in file menu"""
        self.parent.close()

    @staticmethod
    def help_help():
        """Method of the action "help" in help menu"""
        webbrowser.open(
            "https://gitlab.insa-rouen.fr/cip/ubiquity/-/wikis/Mode-d'emploi-de-l'application-%C3%A9tudiante"
        )

    def about_help(self):
        """Method of the action "about" in help menu"""
        AboutDialog(self.parent.view)
