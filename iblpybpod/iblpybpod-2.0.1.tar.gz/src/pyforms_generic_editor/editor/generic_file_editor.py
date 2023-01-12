#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

from confapp import conf


import pyforms
from pyforms.basewidget import BaseWidget

import logging

logger = logging.getLogger(__name__)

try:
	from pyforms.controls import ControlCodeEditor
except:
	logger.error("Could not import ControlCodeEditor. Is QScintilla installed?")


class GenericFileEditor(BaseWidget):
	def __init__(self, path, title, read_only=True):
		self._editor_title = title
		self._read_only = read_only

		BaseWidget.__init__(self, title)

		self.layout().setContentsMargins(5, 5, 5, 5)

		self.path = path

		self.editor = ControlCodeEditor(readonly=read_only)
		self.editor.value = self.content

		self.editor.changed_event = self.__content_changed_evt

	def set_cursor_position(self, line, index):
		self.editor._code_editor.setCursorPosition(line, index)

	def __content_changed_evt(self):
		"""
		
		:return: 
		"""
		self.content = self.editor.value

		self.info("You must restart project to apply changes.", "Restart required.")

		return True

	def beforeClose(self):
		""" 
		Before closing window, ask user if she wants to save (if there are changes)
		
		.. seealso::
			:py:meth:`pyforms.gui.Controls.ControlMdiArea.ControlMdiArea._subWindowClosed`.
		
		"""
		if self.editor.is_modified:
			reply = self.question('Save the changes', 'Save the file', buttons=['cancel','no', 'yes'])

			if reply=='yes':
				self.__content_changed_evt()

	@property
	def content(self):
		if not self.path or not os.path.exists(self.path):
			raise FileNotFoundError("User settings file not found!")
		with open(self.path, "r") as file:
			return file.read()
		return None

	@content.setter
	def content(self, value):
		with open(self.path, "w") as file:
			file.write(value)

	@property
	def title(self):
		return BaseWidget.title.fget(self)

	@title.setter
	def title(self, value):
		BaseWidget.title.fset(self, self._editor_title)


# Execute the application
if __name__ == "__main__":
	pyforms.start_app(SettingsEditor)
