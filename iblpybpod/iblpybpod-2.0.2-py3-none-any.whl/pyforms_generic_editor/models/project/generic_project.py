# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

import pyforms
from pyforms.basewidget import BaseWidget


logger = logging.getLogger(__name__)


class GenericProject(BaseWidget):
	""" ProjectWindow represents the project entity as a GUI window"""

	def __init__(self):
		BaseWidget.__init__(self, 'Generic Project')
		self.layout().setContentsMargins(5, 10, 5, 5)

	def save(self, project_path=None):
		pass

	def save_as(self):
		pass

	def load(self, project_path):
		pass

	def close(self, silent=False):
		pass


# Execute the application
if __name__ == "__main__":
	pyforms.start_app(GenericProject)
