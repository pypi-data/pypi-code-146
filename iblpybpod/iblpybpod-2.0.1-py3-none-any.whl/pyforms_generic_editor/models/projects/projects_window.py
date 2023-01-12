# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from confapp import conf


import pyforms
from pyforms.basewidget import BaseWidget

from pyforms_generic_editor.models.project import Project

logger = logging.getLogger(__name__)

class ProjectsWindow(BaseWidget):
    def __init__(self, mainwindow=None):
        BaseWidget.__init__(self, 'Projects')

        self._projects = []

    def __add__(self, obj):
        self._projects.append(obj)
        return self

    def __sub__(self, obj):
        if isinstance(obj, Project): self._projects.remove(obj)
        return self

    def create_project(self):
        """
        Invoke project creation

        .. seealso::
            * Create project treenode: :class:`pybehavior.models.projects.projects_treenode.ProjectsTreeNode.create_project`.

        :rtype: Project
        """
        pass

    def open_project(self, project_path=None):
        """
        Open project

        .. seealso::
            * Open project treenode: :class:`pybehavior.models.projects.projects_treenode.ProjectsTreeNode.open_project`.

        :param str project_path:
        """
        pass

    def save_all_projects(self):
        for project in self.projects: project.save()

    def save_current_project(self):
        try:
            selected = self.tree.selected_item
            if hasattr(selected, 'window'):
                if issubclass(Project, selected.window.__class__):
                    selected.window.save()
                else:
                    selected.window.project.save()
        except Exception as err:
            logger.warning(err, exc_info=True)
            self.warning(str(err), "Error on saving project")

    def save_current_project_as(self):
        try:
            selected = self.tree.selected_item
            if hasattr(selected, 'window'):
                if issubclass(Project, selected.window.__class__):
                    selected.window.save_as()
                else:
                    selected.window.project.save_as()
        except Exception as err:
            logger.warning(err, exc_info=True)

    def is_saved(self):
        res = True
        for project in self.projects:
            if not project.is_saved():
                res = False
        return res

    @property
    def projects(self):
        return self._projects


if __name__ == "__main__": pyforms.start_app(ProjectsWindow)
