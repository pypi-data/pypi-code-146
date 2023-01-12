# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

import pyforms as app
from pybpodgui_api.exceptions.run_setup import RunSetupError
from pybpodgui_api.models.subject import Subject
from pybpodgui_api.models.subject.subject_com import WrongSubjectConfigured
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlButton
from pyforms.controls import ControlCombo
from pyforms.controls import ControlText
from pyforms_gui.controls.control_checkbox import ControlCheckBox

logger = logging.getLogger(__name__)


class SubjectWindow(Subject, BaseWidget):
    """
    Define here which fields from the board model should appear on the details section.

    The model fields shall be defined as UI components like text fields, buttons, combo boxes, etc.

    You may also assign actions to these components.

    **Properties**

        name
            :class:`string`

            Name associated with this board. Returns the current value stored in the :py:attr:`_name` text field.

        serial_port
            :class:`string`

            Serial port associated with this board. Returns the current value stored in the :py:attr:`_serial_port` text field.


    **Private attributes**

        _name
            :class:`pyforms.controls.ControlText`

            Text field to edit board name. Editing this field fires the event :meth:`BoardWindow._BoardWindow__name_changed_evt`.

        _serial_port
            :class:`pyforms.controls.ControlText`

            Text field to edit serial port. Editing this field fires the event :meth:`BoardWindow._BoardWindow__serial_changed_evt`.

        _log_btn
            :class:`pyforms.controls.ControlButton`

            Button to show this board events on a console window. Pressing the button fires the event :class:`BoardDockWindow.open_log_window`.

        _formset
            Describe window fields organization to PyForms.

    **Methods**

    """

    def __init__(self, project=None):
        """

        :param project: project where this board belongs
        :type project: pycontrolgui.models.project.Project
        """
        BaseWidget.__init__(self, 'Subject')
        self.layout().setContentsMargins(5, 10, 5, 5)

        self._selected_setup = None

        self._name = ControlText('Name')
        self._setups = ControlCombo('Setup')
        self._run = ControlButton('Run', checkable=True, default=self._run_task)

        self._run = ControlButton('Run',
                                  checkable=True,
                                  default=self._run_task,
                                  helptext="When a task is running, you can skip all remaining trials by pressing this button. <br/> <b>NOTE:</b> This means that you will need to break the cycle in your task code when the run_state_machine method returns False.")
        self._kill_task_btn = ControlButton('Kill',
                                            default=self._kill_task,
                                            style="background-color:rgb(255,0,0);font-weight:bold;",
                                            helptext="<b>NOTE:</b>This will exit the task process abruptly. The code you might have after the trial loop won't execute.")

        self._kill_task_btn.enabled = False

        self._stoptrial_btn = ControlButton('Skip trial', default=self._stop_trial_evt)
        self._pause_btn = ControlButton('Pause', checkable=True, default=self._pause_evt)
        self._stoptrial_btn.enabled = False
        self._pause_btn.enabled = False

        self._detached = ControlCheckBox('Detach from GUI', changed_event=self.__detached_changed_evt)

        Subject.__init__(self, project)

        self._formset = [
            '_name',
            '_setups',
            '_detached',
            ('_run', '_kill_task_btn'),
            ('_stoptrial_btn', '_pause_btn'),
            ' ',
        ]

        self._name.changed_event = self.__name_changed_evt
        self.reload_setups()

    def _run_task(self):
        """
        Defines behavior of the button :attr:`SubjectWindow._run_task_btn`.

        This methods is called every time the user presses the button.
        """
        if not self.can_run_task():
            return
        try:
            if self.setup.status == self.setup.STATUS_RUNNING_TASK:
                self.setup.stop_task()
                self._run.enabled = False
            elif self.setup.status == self.setup.STATUS_READY:
                self.setup.run_task()
        except RunSetupError as err:
            self.warning(str(err), "Warning")
        except Exception as err:
            self.alert(str(err), "Unexpected Error")

    def _kill_task(self):
        """
        Kills the currently running task.
        """
        if self.setup.status == self.setup.STATUS_RUNNING_TASK:
            self.setup.kill_task()

    def _stop_trial_evt(self):
        setup = self._setups.value
        if setup:
            setup.stop_trial()
        else:
            self.critical("There isn't any setup selected. Please select one before continuing.", "No setup selected")

    def _pause_evt(self):
        self.pause_trial()

    def can_run_task(self):
        try:
            res = super().can_run_task()
        except WrongSubjectConfigured:
            if self.setup.status == self.setup.STATUS_READY:
                # warn here the user that if he/she pretends to continue, all the other subjects will be removed
                # (only if there aren't any subjects)
                result = self.question("Attention: There are subjects in the selected setup.\nDo you wish to continue?\n\n"
                                       "(note: if you continue all the existing subjects will be replaced)",
                                       "Existing subjects")
                if result == 'yes':
                    self.setup.clear_subjects()
                    res = True
                    self.setup += self
                elif result == 'no':
                    res = False
                else:
                    res = True
            else:
                res = False

        except Exception as e:
            self.warning(str(e), "Error occurred")
            res = False

        if res:
            res = self.setup.can_run_task()
        if not res:
            self._run.checked = False
        return res

    def reload_setups(self):
        tmp = self._setups.value
        self._setups.clear()
        self._setups.add_item('', None)
        for experiment in self.project.experiments:
            for setup in experiment.setups:
                self._setups.add_item(
                    "{experiment} > {setup}".format(experiment=setup.experiment.name, setup=setup.name),
                    setup
                )

        self._setups.value = tmp

    def __detached_changed_evt(self):
        setup = self._setups.value
        if setup:
            setup._detached.value = self._detached.value

    def __name_changed_evt(self):
        """
        React to changes on text field :py:attr:`_name`.

        This methods is called every time the user changes the field.
        """
        if not hasattr(self, '_update_name') or not self._update_name:
            self.name = self._name.value

    def load(self, path):
        try:
            super(Subject, self).load(path)
        except Exception as ex:
            self.warning('{first_arg}'.format(first_arg=ex.args[0]), 'Unable to load a subject')

    @property
    def name(self):
        return self._name.value

    @name.setter
    def name(self, value):
        self._update_name = True  # Flag to avoid recursive calls when editing the name text field
        self._name.value = value
        self._update_name = False

    @property
    def setup(self):
        return self._setups.value

    @setup.setter
    def setup(self, value):
        self._setups.value = value


# Execute the application
if __name__ == "__main__":
    app.start_app(SubjectWindow)
