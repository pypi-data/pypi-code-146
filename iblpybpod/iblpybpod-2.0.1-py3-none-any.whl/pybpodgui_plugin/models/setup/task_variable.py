# !/usr/bin/python3
# -*- coding: utf-8 -*-

from pybpodgui_api.models.setup.task_variable import TaskVariable
from pyforms.controls import ControlCombo


class TaskVariableWindow(TaskVariable):

    def __init__(self, board_task, name=None, value=None, datatype='string'):
        self._varslist = board_task._vars

        self._combo = ControlCombo(None)
        self._combo.add_item('Number', 'number')
        self._combo.add_item('String', 'string')
        self._combo.value = datatype
        self._combo.changed_event = self.__datatype_changed_evt

        self._row_index = self._varslist.rows_count
        self._varslist += [name, self._combo, value]

        TaskVariable.__init__(self, board_task, name, value, datatype)

    def __datatype_changed_evt(self):
        datatype = self._combo.value
        if datatype == 'number':
            item = self._varslist.get_value(2, self._row_index)
            if not item.isnumeric():
                self._varslist.set_value(2, self._row_index, '0')

    def tolist(self):
        return [self.name, self._combo, self.value]

    @property
    def name(self):
        return self._varslist.get_value(0, self._row_index)

    @name.setter
    def name(self, value):
        self._varslist.set_value(0, self._row_index, value)

    @property
    def value(self):
        value = self._varslist.get_value(2, self._row_index)
        return float(value) if self.datatype == 'number' else value

    @value.setter
    def value(self, value): self._varslist.set_value(2, self._row_index, value)

    @property
    def datatype(self): return self._varslist.get_value(1, self._row_index).value

    @datatype.setter
    def datatype(self, value):  self._varslist.get_value(1, self._row_index).value = value
