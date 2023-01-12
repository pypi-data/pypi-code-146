"""Module managing the open dialog"""
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

import time
from tkinter import ttk, messagebox
from tkinter.constants import RIGHT, END, BOTTOM, Y, BOTH, EW, DISABLED, NORMAL, BROWSE, YES
from typing import Optional

from .base import BaseDialog
from ...utils import LabelEnum
from ....controllers.config_file import Config


class OpenDialog(BaseDialog):
    """Class for the open dialog"""
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config
        self.tree: Optional[ttk.Treeview] = None
        self.open_button = None
        self.delete_button = None
        super().__init__(parent, LabelEnum.RECENTLY_OPEN.value)

    def _event_setup(self):
        self.bind("<Return>", self.open)
        self.bind('<<TreeviewSelect>>', self._select_changed)

    def _ui_setup(self):
        self.geometry('275x250')
        self.minsize(275, 250)
        scrollbar = ttk.Scrollbar(self)
        scrollbar.pack(side=RIGHT, fill=Y)
        # Create listbox
        self.tree = ttk.Treeview(self, columns=('id', Config.DATE, Config.NAME), show='headings',
                                 yscrollcommand=scrollbar.set, selectmode=BROWSE, height=5)

        self.tree.heading(0, text='Id', command=lambda: self._sort_column(0, lambda t: t[0], True))
        self.tree.column(0, minwidth=20, width=25)
        self.tree.heading(1, text='Date', command=lambda: self._sort_column(1, lambda t: time.mktime(
            time.strptime(t[0], "%d/%m/%Y")), False))
        self.tree.column(1, minwidth=70, width=70)
        self.tree.heading(2, text='Name', command=lambda: self._sort_column(2, lambda t: t[0], False))
        self.tree.column(2, minwidth=100, width=100)
        scrollbar.config(command=self.tree.yview)
        self.tree.pack(fill=BOTH, expand=YES)
        self._init_treeview()

        # Create button
        mainframe = ttk.Frame(self, padding="3 3 12 12")
        mainframe.pack(side=BOTTOM, pady=5, padx=5)
        self.open_button = ttk.Button(mainframe, text=LabelEnum.OPEN.value, command=self.open, state=DISABLED)
        self.open_button.grid(column=0, row=0, sticky=EW)
        self.delete_button = ttk.Button(mainframe, text=LabelEnum.DELETE.value, command=self.delete, state=DISABLED)
        self.delete_button.grid(column=1, row=0, sticky=EW, padx=5)
        ttk.Button(mainframe, text=LabelEnum.CANCEL.value, command=self.dismiss).grid(column=2, row=0, sticky=EW)

    def _init_treeview(self):
        """Method initializing the listbox"""
        history = self.config.configs[Config.HISTORY].copy()
        if Config.DEFAULT in history:
            history.pop(Config.DEFAULT)
        for num, key in enumerate(history.keys(), 1):
            self.tree.insert('', END, values=(num, history[key][Config.DATE] if Config.DATE in history[key] else '',
                                              history[key][Config.NAME]))

    def open(self, *_):
        """Method opening config for the open button"""
        selection = self.tree.selection()
        if len(selection) == 1:
            index = int(self.tree.item(selection)['values'][0])-1
            config = self._get_config(index)
            self.parent.model.server.set(config[Config.SERVER])
            self.parent.model.student_key.set(config[Config.STUDENT_KEY])
            self.parent.model.group_key.set(config[Config.GROUP_KEY])
            self.parent.model.directory.set(config[Config.DIRECTORY])
            self.is_valid = self.parent.submit()
            self.dismiss()
            if not self.is_valid:
                messagebox.showerror(message=self.parent.model.error.get())
        else:
            self.dismiss()

    def delete(self):
        """Method deleting config for the delete button"""
        selection = self.tree.selection()
        if len(selection) == 1:
            index = int(self.tree.item(selection)['values'][0])-1
            config = self._get_config(index)
            if messagebox.askyesno(title=LabelEnum.DELETE.value, message=LabelEnum.DELETE_YES_NO.value % {
                'num': str(index+1),
                'name': str(config[Config.NAME])
            }):
                self.parent.model.server.set(config[Config.SERVER])
                self.parent.model.student_key.set(config[Config.STUDENT_KEY])
                self.parent.model.group_key.set(config[Config.GROUP_KEY])
                self.parent.model.directory.set(config[Config.DIRECTORY])
                self.config.remove_config(self.parent.model)
                self.tree.delete(selection)
                self.parent.model.server.set("")
                self.parent.model.student_key.set("")
                self.parent.model.group_key.set("")
                self.parent.model.directory.set("")
                self._select_changed()

    def _select_changed(self, *_):
        if len(self.tree.selection()) == 1:
            self.open_button['state'] = NORMAL
            self.delete_button['state'] = NORMAL
        else:
            self.open_button['state'] = DISABLED
            self.delete_button['state'] = DISABLED

    def _get_config(self, index: int):
        history = self.config.configs[Config.HISTORY].copy()
        if Config.DEFAULT in history:
            history.pop(Config.DEFAULT)
        key = list(history.keys())[index]
        return self.config.configs[Config.HISTORY][key]

    def _sort_column(self, column, function, reverse):
        elements = [(self.tree.item(children_id)["values"][column], children_id)
                    for children_id in self.tree.get_children()]
        elements.sort(key=function, reverse=reverse)
        for value, (_, index) in enumerate(elements):
            self.tree.move(index, '', value)
        self.tree.heading(column, command=lambda: self._sort_column(column, function, not reverse))
