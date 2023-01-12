# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from confapp import conf

from AnyQt.QtGui import QIcon

from pybpodgui_api.models.setup import Setup
from pybpodgui_plugin.models.setup.setup_com import SetupCom

logger = logging.getLogger(__name__)


class SetupUIBusy(SetupCom):
    """
    Extends setup with UI refreshment logic.

    .. seealso::
        UI buttons: :py:class:`pybpodgui_plugin.models.setup.setup_window.SetupWindow`.

    **Methods**

    """

    def stop_trial(self):
        super(SetupUIBusy, self).stop_trial()
        self._pause_btn.label = 'Pause'
        self._pause_btn.checked = False

    def pause_trial(self):
        super(SetupUIBusy, self).pause_trial()
        self._pause_btn.label = 'Resume'

    def resume_trial(self):
        super(SetupUIBusy, self).resume_trial()
        self._pause_btn.label = 'Pause'

    def stop_task(self):
        super(SetupUIBusy, self).stop_task()
        self._run_task_btn.enabled = False

    def kill_task(self):
        super(SetupUIBusy, self).kill_task()
        self._kill_task_btn.enabled = False

    def update_ui(self):
        """
        Update UI button states and labels and tree icons when board communication is active.
        """
        if not hasattr(self, 'node'):
            return

        logger.debug('Setup [{0}] status: {1}'.format(self.name, self.status))

        if self.status == Setup.STATUS_READY:

            self.node.setIcon(0, QIcon(conf.BOX_SMALL_ICON))

            self._run_task_btn.label = 'Run'
            self._run_task_btn.checked = False
            self._run_task_btn.enabled = True

            self._kill_task_btn.enabled = False

            self._stoptrial_btn.enabled = False
            self._pause_btn.label = 'Pause'
            self._pause_btn.enabled = False
            self._pause_btn.checked = False

            self._board.enabled = True
            self._detached.enabled = True
            self._task.enabled = True

        elif self.status == Setup.STATUS_BOARD_LOCKED:

            self.node.setIcon(0, QIcon(conf.BUSY_SMALL_ICON))
            # self.disable_all_task_buttons()
            self._board.enabled = False
            self._task.enabled = False

        elif self.status == Setup.STATUS_RUNNING_TASK:

            self._run_task_btn.label = 'Stop'
            self._run_task_btn.checked = True

            self._kill_task_btn.enabled = True

            self._stoptrial_btn.enabled = True
            self._pause_btn.enabled = True

            self.node.setIcon(0, QIcon(conf.PLAY_SMALL_ICON))
            # self.disable_all_task_buttons()
            self._board.enabled = False
            self._task.enabled = False
            self._detached.enabled = False

        self.board_task.update_ui()
        if self.last_session:
            self.last_session.update_ui()

    def enable_all_task_buttons(self):
        """
        Enable UI buttons for upload task, configure task and run task
        """
        self._run_task_btn.enabled = True

    def disable_all_task_buttons(self):
        """
        Disable UI buttons for upload task, configure task and run task
        """
        self._run_task_btn.enabled = False
