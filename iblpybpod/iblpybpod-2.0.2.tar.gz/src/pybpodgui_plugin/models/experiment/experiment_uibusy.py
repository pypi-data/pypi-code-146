# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from confapp import conf

from AnyQt.QtGui import QIcon

from pybpodgui_api.models.setup import Setup
from pybpodgui_plugin.models.experiment.experiment_dockwindow import ExperimentDockWindow

logger = logging.getLogger(__name__)


class ExperimentUIBusy(ExperimentDockWindow):
    """
    Extends experiment with UI refreshment logic.

    .. seealso::
        UI buttons: :py:class:`pybpodgui_plugin.models.experiment.experiment_window.ExperimentWindow`.

    **Methods**

    """

    def __init__(self, project):
        super(ExperimentUIBusy, self).__init__(project)
        self.__running_icon = QIcon(conf.PLAY_SMALL_ICON)

    ############################################################################

    def update_ui(self):
        """
        Update UI button states and labels and tree icons when board communication is active.
        """
        busy_status = Setup.STATUS_READY

        # Check first if any setup is busy
        for setup in self.setups:
            if setup.status > Setup.STATUS_BOARD_LOCKED:
                busy_status = setup.status
                break

        # if there is no setups busy, will test if the boards are locked
        if busy_status == Setup.STATUS_READY:
            for setup in self.setups:
                if setup.status > Setup.STATUS_READY:
                    busy_status = setup.status
                    break

        logger.debug('Experiment [{0}] status:{1}'.format(self.name, busy_status))

        if busy_status == Setup.STATUS_READY:

            self.node.setIcon(0, QIcon(conf.EXPERIMENT_SMALL_ICON))
            # if self.task:
            # 	self.enable_all_task_buttons()
            # else:
            # 	self.disable_all_task_buttons()
            # self._task.enabled = True

        elif busy_status == Setup.STATUS_BOARD_LOCKED:

            self.node.setIcon(0, QIcon(conf.BUSY_SMALL_ICON))
            self.disable_all_task_buttons()
            # self._task.enabled = False

        elif busy_status == Setup.STATUS_RUNNING_TASK:

            self.node.setIcon(0, QIcon(conf.PLAY_SMALL_ICON))
            self.disable_all_task_buttons()
            # self._task.enabled = False

        for setup in self.setups:
            setup.update_ui()

    def enable_all_task_buttons(self):
        """
        Enable UI buttons for restore task variables, upload task and run task
        """
        # self._button_run_all.enabled = True
        pass

    def disable_all_task_buttons(self):
        """
        Disable UI buttons for restore task variables, upload task and run task
        """
        # self._button_run_all.enabled = False
        pass
