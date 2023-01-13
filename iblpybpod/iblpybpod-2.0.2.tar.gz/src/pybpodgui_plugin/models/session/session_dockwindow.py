# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from pybpodgui_plugin.models.session.session_treenode import SessionTreeNode

logger = logging.getLogger(__name__)


class SessionDockWindow(SessionTreeNode):

    def show(self):
        self.mainwindow.details.value = self
        super(SessionDockWindow, self).show()

    @property
    def mainwindow(self):
        return self.setup.mainwindow

    def beforeClose(self):
        return False
