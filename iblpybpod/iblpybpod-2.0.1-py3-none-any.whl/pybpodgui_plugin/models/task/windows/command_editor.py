#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pyforms
import os
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlTreeView
from pyforms.controls import ControlButton
from pyforms.controls import ControlText
from pyforms.controls import ControlCombo
from pathlib import Path

from AnyQt.QtWidgets import QFileSystemModel

from pybpodgui_api.models.task.taskcommand import TaskCommand


class CommandEditor(BaseWidget):

    def __init__(self, task=None, when=None, command=None):
        title = "Post command editor" if when == TaskCommand.WHEN_POST else "Pre command editor"
        BaseWidget.__init__(self, title, parent_win=task)
        self.command = command
        self.task = task
        self.when = when
        self.set_margin(5)

        self._type = ControlCombo('Type of command', changed_event=self.__type_changed_evt)
        self._cancelbtn = ControlButton('Cancel', default=self.__cancel_evt)
        self._okbtn = ControlButton('Ok', default=self.__ok_evt)

        self._command = ControlText('External command', visible=False)
        self._filesbrowser = ControlTreeView('Files browser')

        self._type.add_item('Execute a gui script', 'script')
        self._type.add_item('Execute a external command', 'external')

        self.formset = [
            '_type',
            '_command',
            '_filesbrowser',
            (' ', '_cancelbtn', '_okbtn'),
            ' '
        ]

        root_path = os.path.abspath(task.path if task else '/')
        self.syspath_model = QFileSystemModel(self)
        self.syspath_model.setRootPath(root_path)
        self.syspath_model.setNameFilters(['*.py'])
        self.syspath_model.setNameFilterDisables(False)
        self._filesbrowser.value = self.syspath_model

        root_index = self.syspath_model.index(root_path)
        self._filesbrowser.setRootIndex(root_index)
        for i in range(1, 4):
            self._filesbrowser.hideColumn(i)

    def __type_changed_evt(self):
        if self._type.value == 'script':
            self._filesbrowser.show()
            self._command.hide()
        elif self._type.value == 'external':
            self._filesbrowser.hide()
            self._command.show()

    def __cancel_evt(self):
        self.close()
        self.task.cmdwin = None

    def __ok_evt(self):

        if self.command is not None:
            command = self.command
        else:
            command = self.task.create_scriptcmd() if self._type.value == 'script' else self.task.create_execcmd()
            command.when = self.when

        if self._type.value == 'script':
            for index in self._filesbrowser.selectedIndexes():
                filepath = self.syspath_model.filePath(index)
                break
            if filepath is None:
                return

            file_path = Path(filepath)
            task_path = Path(self.task.path)
            relpath = file_path.relative_to(task_path)
            command.script = str(relpath)

        elif self._type.value == 'external':
            command.cmd = self._command.value

        self.task.update_commands()
        self.close()
        self.task.cmdwin = None


if __name__ == "__main__":
    pyforms.start_app(CommandEditor)
