# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from confapp import conf

from pyforms_generic_editor.models.projects.projects_treenode import ProjectsTreeNode

logger = logging.getLogger(__name__)


class ProjectsDockWindow(ProjectsTreeNode):
	def __init__(self, mainwindow=None):
		ProjectsTreeNode.__init__(self, mainwindow)

		self.mainwindow = mainwindow
		self.mainwindow.dock.value = self

		self.register_on_toolbar(self.mainwindow.toolbar)
		self.register_on_main_menu(self.mainwindow.mainmenu)

	def register_on_toolbar(self, toolbar):
		pass

	def register_on_main_menu(self, mainmenu):
		filemenu = mainmenu[0]
		filemenu['File'].insert(0, {'New project': self.create_project, 'icon': conf.NEW_SMALL_ICON})
		filemenu['File'].insert(1, '-')
		filemenu['File'].insert(2, {'Open a project': self._option_open_project, 'icon': conf.OPEN_SMALL_ICON})
		filemenu['File'].insert(3, '-')
		filemenu['File'].insert(4,
		                        {'Save current project': self.save_current_project, 'icon': conf.SAVE_SMALL_ICON})
		filemenu['File'].insert(5, {'Save current project as': self.save_current_project_as,
		                            'icon': conf.SAVE_SMALL_ICON})
		filemenu['File'].insert(6, {'Save all projects': self.save_all_projects, 'icon': conf.SAVE_SMALL_ICON})
		filemenu['File'].insert(7, '-')

	def _option_open_project(self):
		try:
			self.open_project()
		except Exception as err:
			for project in self.projects:
				project.close(silent=True)

			logger.warning(str(err), exc_info=True)
			self.warning(str(err), "Invalid project path")
