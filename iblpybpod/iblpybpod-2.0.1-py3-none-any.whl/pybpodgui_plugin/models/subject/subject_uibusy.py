# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from confapp import conf

from AnyQt.QtGui import QIcon

from pybpodgui_plugin.models.subject.subject_dockwindow import SubjectDockWindow

logger = logging.getLogger(__name__)


class SubjectUIBusy(SubjectDockWindow):
    """
    Extends subject with UI refreshment logic.

    """

    def __init__(self, project):
        super(SubjectUIBusy, self).__init__(project)
        self.__running_icon = QIcon(conf.PLAY_SMALL_ICON)

    def pause_trial(self):
        setup = self._setups.value
        if setup:
            if self._pause_btn.checked:
                setup.pause_trial()
                self._pause_btn.label = 'Resume'
            else:
                setup.resume_trial()
                self._pause_btn.label = "Pause"

    # This must switch between start and stop
    def update_ui(self, sessionrunning=False):
        if sessionrunning:
            self._run.checked = True
            self._run.label = 'Stop'
            self._kill_task_btn.enabled = True
            self._stoptrial_btn.enabled = True
            self._pause_btn.enabled = True
            self._detached.enabled = False
            for sess in self._sessions:
                if sess.running:
                    self.node.setIcon(0, self.__running_icon)
        else:
            self._run.checked = False
            self._run.label = 'Run'
            self._kill_task_btn.enabled = False
            self._detached.enabled = True
            self._stoptrial_btn.enabled = False
            self._pause_btn.enabled = False
            self._pause_btn.checked = False
            self.node.setIcon(0, QIcon(conf.SUBJECT_SMALL_ICON))
