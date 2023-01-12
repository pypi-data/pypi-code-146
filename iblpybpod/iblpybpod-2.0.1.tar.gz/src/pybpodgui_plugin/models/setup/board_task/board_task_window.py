#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import re

import pyforms as app
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlList
from pyforms.controls import ControlCheckBox

from pybpodgui_plugin.models.setup.task_variable import TaskVariableWindow
from pybpodgui_api.models.setup.board_task import BoardTask

logger = logging.getLogger(__name__)


class BoardTaskWindow(BoardTask, BaseWidget):
    """
    Define here which fields from the board_task model should appear on the setup configuration window.

    The model fields shall be defined as UI components like text fields, buttons, combo boxes, etc.

    You may also assign actions to these components.

    .. seealso::
        This class heavy relies on the corresponding API module.

        :py:class:`pybpodgui_api.models.setup.board_task.BoardTask`

    **Properties**

        states
            A list of task states associated with this BoardTask. States are defined on the task code.

        events
            A list of task events associated with this BoardTask. Events are defined on the task code.

        variables
            A list of task variables associated with this BoardTask. Variables are defined on the task code.

    **Private attributes**

        _states
            :class:`pyforms.controls.ControlList`

            UI list to show BoardTask states.

        _events
            :class:`pyforms.controls.ControlList`

            UI list to show BoardTask events.

        _vars
            :class:`pyforms.controls.ControlList`

            UI list to show BoardTask variables.

        _sync_btn
            :class:`pyforms.controls.ControlButton`

            Button to sync variables with board. Pressing the button fires the event :meth:`BoardTaskWindow.sync_variables`.

        _load_btn
            :class:`pyforms.controls.ControlButton`

            Button to read task variables from board. Pressing the button fires the event :meth:`BoardTaskWindow._BoardTaskWindow__load_task_details`.

        _formset
            Describe window fields organization to PyForms.

    **Methods**

    """

    def __init__(self, setup):
        BaseWidget.__init__(self, "Variables config for {0}".format(setup.name))

        self._var_is_being_added = False

        self._updvars = ControlCheckBox('Update variables')
        self._vars = ControlList('Variables',
                                 add_function=self.__add_variable,
                                 remove_function=self.__remove_variable)

        BoardTask.__init__(self, setup)

        self._vars.horizontal_headers = ['NAME', 'TYPE', 'VALUE']
        self._vars.data_changed_event = self.__varslist_data_changed_evt

        self._formset = ['_updvars', '_vars']

        self._variable_rule = re.compile('^[A-Z0-9\_]+$')

    @property
    def update_variables(self):
        return self._updvars.value

    @update_variables.setter
    def update_variables(self, value):
        self._updvars.value = value

    def create_variable(self, name=None, value=None, datatype='string'):
        return TaskVariableWindow(self, name, value, datatype)

    def __varslist_data_changed_evt(self, row, col, item):

        # only verify if the list is being edited
        if self._var_is_being_added is True:
            return

        if col == 0 and item is not None:
            if not (self._variable_rule.match(item) and item.startswith('VAR_')):
                self.critical("The name of the variable should start with VAR_, should be alphanumeric and upper case.",
                              "Error")

                self._vars.set_value(
                    col, row,
                    'VAR_{0}'.format( self._vars.rows_count))

        elif col == 2:
            datatype_combo = self._vars.get_value(1, row)
            datatype = datatype_combo.value if datatype_combo else None
            if datatype == 'number' and isinstance(item, str) and not item.isnumeric():
                self.message("The value should be numeric.", "Error")
                self._vars.set_value(
                    col, row,
                    '0'
                )

    def __add_variable(self):
        self._var_is_being_added = True
        var = self.create_variable(
            'VAR_{0}'.format(self._vars.rows_count),
            '0'
        )
        self._var_is_being_added = False

    def __remove_variable(self):
        if self._vars.selected_row_index is not None:
            var = self.variables[self._vars.selected_row_index]
            self.variables.remove(var)
            self._vars -= -1

    def before_close(self):
        return False


# Execute the application
if __name__ == "__main__":
    app.start_app(BoardTaskWindow)
