# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from pybpodgui_plugin.models.project.project_treenode import ProjectTreeNode

logger = logging.getLogger(__name__)


class ProjectDockWindow(ProjectTreeNode):
    def show(self):
        self.mainwindow.details.value = self
        super(ProjectDockWindow, self).show()

    def focus_name(self):
        """
        Sets interface focus on the board name text field
        """
        self._name.form.lineEdit.setFocus()

    def close(self, silent=False):
        self.mainwindow.details.value = None
        super(ProjectDockWindow, self).close(silent)

    @property
    def mainwindow(self):
        return self.projects.mainwindow
