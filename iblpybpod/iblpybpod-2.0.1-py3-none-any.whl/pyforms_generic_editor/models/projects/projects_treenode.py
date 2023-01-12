# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from pyforms.controls import ControlTree

from pyforms_generic_editor.models.projects.projects_window import ProjectsWindow

logger = logging.getLogger(__name__)


class ProjectsTreeNode(ProjectsWindow):
	def __init__(self, mainwindow=None):
		ProjectsWindow.__init__(self, mainwindow)

		self.tree = ControlTree('Projects')

		self.tree.item_selection_changed_event = self.__item_sel_changed_evt
		self.clear()

	def __item_sel_changed_evt(self):
		"""
		Show window from selected node (if exists)
		"""
		try:
			selected = self.tree.selected_item
			if hasattr(selected, 'window'):
				selected.window.show()
		except Exception as err:  # CATCH UNEXPECTED ERRORS FROM WINDOWS PREVENTING APP KILL
			logger.error(str(err), exc_info=True)

	def clear(self):
		self.tree.setDragEnabled(False)
		self.tree.show_header = False
		# self.tree.setHeaderLabel('Please open or create project')
		self.tree.clear()

	def create_project(self):
		"""
		Invoke project creation and focus GUI on the new tree node.

		.. seealso::
			* Create project: :class:`pybehavior.models.projects.projects_window.ProjectsWindow.create_project`.

		:rtype: Project
		"""
		pass

	def open_project(self, project_path=None):
		"""
		Open project. We want to temporarily silent the item_selection_changed_event becasue otherwise, when loading
		the project, entities will show up on the MDI area (and not in the dockwindow).
		Finally, we have to force the project node to change.

		.. seealso::
			* Open project: :class:`pybehavior.models.projects.projects_window.ProjectsWindow.open_project`.

		:param str project_path:
		"""
		pass
