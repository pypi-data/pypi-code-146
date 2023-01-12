# !/usr/bin/python3
# -*- coding: utf-8 -*-


from pybpodgui_plugin.models.projects.projects_window import ProjectsWindow
from pybpodgui_plugin import utils


class ProjectsTreeNode(ProjectsWindow):

    def create_project(self):
        """
        Invoke project creation and focus GUI on the new tree node.

        .. seealso::
            * Create project: :class:`pybpodgui_plugin.models.projects.projects_window.ProjectsWindow.create_project`.

        :rtype: Project
        """
        project = super().create_project()
        self.tree.setCurrentItem(project.node)
        project.focus_name()
        return project

    def open_project(self, project_path=None):
        """
        Open project. We want to temporarily silent the item_selection_changed_event becasue otherwise, when loading
        the project, entities will show up on the MDI area (and not in the dockwindow).
        Finally, we have to force the project node to change.

        .. seealso::
            * Open project: :class:`pybpodgui_plugin.models.projects.projects_window.ProjectsWindow.open_project`.

        :param str project_path:
        """
        try:
            self.tree.item_selection_changed_event = utils.do_nothing
            project = super().open_project(project_path)
            if project:
                self.tree.item_selection_changed_event = self.__item_sel_changed_evt
                self.tree.setCurrentItem(project.node)
                self.__item_sel_changed_evt()
            return project
        except Exception:
            self.tree.item_selection_changed_event = self.__item_sel_changed_evt
            raise
