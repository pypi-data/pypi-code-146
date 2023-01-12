# !/usr/bin/python3
# -*- coding: utf-8 -*-

from pybpodgui_plugin.models.session.session_dockwindow import SessionDockWindow


class SessionSignals(SessionDockWindow):
    """
    Session Signals offers a set of useful pyqt signals
    """

    def create_treenode(self, tree):
        super().create_treenode(tree)

        self.project.projects.signal_session_create_treenode.emit(self)
