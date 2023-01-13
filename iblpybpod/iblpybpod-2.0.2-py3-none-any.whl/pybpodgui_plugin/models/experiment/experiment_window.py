# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

import pyforms as app
from pybpodgui_plugin.models.setup import Setup
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlText
from pyforms.controls import ControlButton
from pybpodgui_api.models.experiment import Experiment
from pybpodgui_api.models.project import Project

logger = logging.getLogger(__name__)


class ExperimentWindow(Experiment, BaseWidget):
    """
    Define here which fields from the board model should appear on the details section.

    The model fields shall be defined as UI components like text fields, buttons, combo boxes, etc.

    You may also assign actions to these components.

    **Private attributes**

    _name
        Field to edit experiment name

        :type: :class:`pyforms.controls.ControlText`

    _task
        Combo box of available tasks. Current selected task is the task associated for this experiment
        and all its setups. Selecting a different task fires the event :class:`ExperimentWindow._ExperimentWindow__task_changed_evt`.

        :type: :class:`pyforms.controls.ControlCombo`

    **Methods**

    """

    def __init__(self, project):
        # type: (Project) -> None
        """

        :param project: project where this experiment belongs
        :type project: pycontrolgui.models.project.Project
        """
        BaseWidget.__init__(self, 'Experiment')
        self.layout().setContentsMargins(5, 10, 5, 5)

        self._name = ControlText('Exp. name')
        # self._task     = ControlCombo('Protocol', changed_event=self.__task_changed_evt)
        self._runsetup = ControlButton('Run all')

        self._formset = [
            '_name',
            # '_task',
            '_runsetup',
            ' '
        ]

        Experiment.__init__(self, project)

        # self.reload_tasks()

        self._name.changed_event = self.__name_changed_evt
        self._runsetup.value = self.__run_all

    def __run_all(self):
        for setup in self.setups:
            setup._run_task()

    def __task_changed_evt(self):
        """

        This methods is called every time the user presses the button.
        """
        # self.task = self._task.value
        # self.update_ui()

    def __name_changed_evt(self):
        if not hasattr(self, '_update_name') or not self._update_name:
            self.name = self._name.value

    def __sub__(self, obj):
        res = super().__sub__(obj)

        if isinstance(obj, Setup):
            for subject in self.project.subjects:
                subject.reload_setups()

        return res

    @property
    def name(self):
        return self._name.value

    @name.setter
    def name(self, value):
        self._update_name = True  # Flag to avoid recurse calls when editing the name text field
        self._name.value = value
        self._update_name = False


if __name__ == "__main__":
    # Execute the application
    app.start_app(ExperimentWindow)
