# !/usr/bin/python3
# -*- coding: utf-8 -*-

from confapp import conf

from AnyQt.QtGui import QIcon

from pybpodgui_api.models.setup import Setup
from pybpodgui_plugin.models.session.session_signals import SessionSignals


class SessionUIBusy(SessionSignals):
    """

    """

    def update_ui(self):
        """

        """
        if not hasattr(self, 'node'):
            return

        if self.setup.status in [
            Setup.STATUS_RUNNING_TASK
        ]:
            self.node.setIcon(0, QIcon(conf.PLAY_SMALL_ICON))
            for s in self.subjects_nodes.values():
                s.setIcon(0, QIcon(conf.PLAY_SMALL_ICON))
            self.running = True
        else:
            self.node.setIcon(0, QIcon())
            for s in self.subjects_nodes.values():
                s.setIcon(0, QIcon())
            self.running = False
