# !/usr/bin/python3
# -*- coding: utf-8 -*-

import pyforms
from confapp import conf

from AnyQt.QtWidgets import QFileDialog
from AnyQt.QtCore import pyqtSignal

from pybpodgui_plugin.models.project import Project
from pybpodgui_plugin.models.session import Session

from pyforms.controls import ControlToolButton


class ProjectsWindow(object):
    """
    See:
     - pyforms_generic_editor.models.projects.__init__.py
     - pyforms_generic_editor.models.projects.projects_window.py
    """

    signal_session_create_treenode = pyqtSignal(Session)

    def __init__(self, mainwindow=None):
        super(ProjectsWindow, self).__init__(mainwindow)

    def register_on_toolbar(self, toolbar):
        toolbar += [
            ControlToolButton(
                'New',
                icon=conf.NEW_SMALL_ICON,
                default=self.create_project,
                maxheight=30
            ),
            ControlToolButton(
                'Open',
                icon=conf.OPEN_SMALL_ICON,
                default=self._option_open_project,
                maxheight=30
            ),
            ControlToolButton(
                'Save',
                icon=conf.SAVE_SMALL_ICON,
                default=self.save_current_project,
                maxheight=30
            ), '|'
        ]

    def create_project(self):
        """
        Invoke project creation

        .. seealso::
            * Create project treenode: :class:`pybpodgui_plugin.models.projects.projects_treenode.ProjectsTreeNode.create_project`.

        :rtype: Project
        """
        return Project(self)

    def open_project(self, project_path=None):
        """
        Open project

        .. seealso::
            * Open project treenode: :class:`pybpodgui_plugin.models.projects.projects_treenode.ProjectsTreeNode.open_project`.

        :param str project_path:
        """
        project = None
        if not project_path:
            project_path = QFileDialog.getExistingDirectory(self, "Select the project directory")
        if project_path:
            project = self.create_project()
            project.load(str(project_path))

        return project


if __name__ == "__main__":
    pyforms.start_app(ProjectsWindow)
