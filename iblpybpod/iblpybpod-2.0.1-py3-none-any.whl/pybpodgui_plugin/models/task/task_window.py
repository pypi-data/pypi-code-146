# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

import pyforms as app
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlText
from pyforms.controls import ControlCheckBox
from pyforms.controls import ControlList

from pybpodgui_api.models.task import Task
from pybpodgui_plugin.models.task.windows.command_editor import CommandEditor


from pybpodgui_api.models.task.taskcommand import TaskCommand

logger = logging.getLogger(__name__)


class TaskWindow(Task, BaseWidget):
    """
    Define here which fields from the task model should appear on the details section.

    The model fields shall be defined as UI components like text fields, buttons, combo boxes, etc.

    You may also assign actions to these components.

    **Properties**

        name
            :class:`string`

            Name associated with this task. Returns the current value stored in the :py:attr:`_name` text field.

    **Private attributes**

        _name
            :class:`pyforms.controls.ControlText`

            Text field to edit task name. Editing this field fires the event :meth:`TaskWindow._TaskWindow__name_edited_evt`.

        _edit_btn
            :class:`pyforms.controls.ControlButton`

            Button to edit task code. Pressing the button fires the event :meth:`BoardWindow._BoardWindow__install_framework_btn_evt`.

        _formset
            Describe window fields organization to PyForms.

    **Methods**

    """

    def __init__(self, project=None):
        BaseWidget.__init__(self, 'Task')
        self.layout().setContentsMargins(5, 10, 5, 5)

        self.precmdwin = None
        self.postcmdwin = None

        self._namefield = ControlText('Task name', changed_event=self.__name_edited_evt)
        self._use_server = ControlCheckBox('Trigger soft codes using a UDP port')
        self._precmds = ControlList(
            'Pre commands',
            add_function=self.__add_pre_command,
            remove_function=self.__remove_pre_command,
            readonly=True
        )
        self._postcmds = ControlList(
            'Post commands',
            add_function=self.__add_post_command,
            remove_function=self.__remove_post_command,
            readonly=True
        )

        self._formset = [
            '_namefield',
            '_use_server',
            '_precmds',
            '_postcmds',
            ' '
        ]

        Task.__init__(self, project)

        self.update_commands()

    def update_commands(self):
        self._precmds.clear()
        self._postcmds.clear()

        self._precommands_list = []
        self._postcommands_list = []

        for cmd in self.commands:
            if cmd.when == TaskCommand.WHEN_PRE:
                self._precmds += [str(cmd)]
                self._precommands_list.append(cmd)
            elif cmd.when == TaskCommand.WHEN_POST:
                self._postcmds += [str(cmd)]
                self._postcommands_list.append(cmd)

    def __add_pre_command(self):
        if self.precmdwin is not None:
            self.precmdwin.show()
            self.precmdwin.activateWindow()
            self.precmdwin.raise_()
        else:
            self.precmdwin = CommandEditor(self, when=TaskCommand.WHEN_PRE)
            self.precmdwin.show()

    def __remove_pre_command(self):
        row = self._precmds.selected_row_index
        if row is not None:
            obj = self._precommands_list.pop(row)
            self._commands.remove(obj)
            self._precmds -= -1

    def __add_post_command(self):
        if self.postcmdwin is not None:
            self.postcmdwin.show()
            self.postcmdwin.activateWindow()
            self.postcmdwin.raise_()
        else:
            self.postcmdwin = CommandEditor(self, when=TaskCommand.WHEN_POST)
            self.postcmdwin.show()

    def __remove_post_command(self):
        row = self._postcmds.selected_row_index
        if row is not None:
            obj = self._postcommands_list.pop(row)
            self._commands.remove(obj)
            self._postcmds -= -1

    def __use_server_changed_evt(self):
        self._netport.enabled = True if self._use_server.value else False

    def __name_edited_evt(self):
        """
        React to changes on text field :py:attr:`_name`.

        This methods is called every time the user changes the field.
        """
        if not hasattr(self, '_update_name') or not self._update_name:
            self.name = self._namefield.value

    @property
    def name(self): return Task.name.fget(self)

    @name.setter
    def name(self, value):
        try:
            Task.name.fset(self, value)
        except FileNotFoundError as e:
            self.critical(str(e), 'File not found')
        # Flag to avoid recurse calls when editing the name text field
        self._update_name = True
        self._namefield.value = value
        self._update_name = False

    @property
    def trigger_softcodes(self):
        return self._use_server.value

    @trigger_softcodes.setter
    def trigger_softcodes(self, value):
        self._use_server.value = (value is True)

    def load(self, path):
        super(TaskWindow, self).load(path)
        self.update_commands()


# Execute the application
if __name__ == "__main__":
    app.start_app(TaskWindow)
