# !/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import logging

from confapp import conf

import pkgutil

from AnyQt.QtWidgets import qApp, QMessageBox
from AnyQt.QtGui import QIcon

from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlMdiArea

from pyforms_generic_editor.editor.generic_file_editor import GenericFileEditor

logger = logging.getLogger(__name__)


class SafeModeEditor(BaseWidget):
	def __init__(self):

		global conf
		conf += 'pyforms_generic_editor.resources'

		BaseWidget.__init__(self, conf.GENERIC_EDITOR_TITLE)

		self.mdi_area = ControlMdiArea()

		self.mainmenu = [
			{'File': [
				{'Exit': self._exit_app, 'icon': QIcon(conf.EXIT_SMALL_ICON)}
			]},
			{'Options': [
				{'Edit user settings': self._edit_user_settings, 'icon': QIcon(conf.USER_SETTINGS_ICON)}
			]},
			{'Help': [  # this option works for OSX also
				{'About QT': self._option_about_qt},
				{'About the application': self._option_about}
			]}
		]

		self._edit_user_settings()
		self._show_app_log()

		self.mdi_area.tileSubWindows()

	def init_form(self):
		error_message = conf.GENERIC_EDITOR_LOAD_EXCEPTION_TRACEBACK

		msg = QMessageBox()
		msg.setIcon(QMessageBox.Critical)

		msg.setText("Invalid settings file")
		msg.setInformativeText("Please correct user settings file.")
		msg.setWindowTitle("Invalid settings file")
		msg.setDetailedText(error_message)
		msg.setStandardButtons(QMessageBox.Ok)

		retval = msg.exec_()

		super(SafeModeEditor, self).init_form()

	def _option_about_qt(self):
		self.aboutQt("About Qt")

	def _option_about(self):
		msg = "About {0}\n".format(self.title)
		for module in self.dependencies:
			msg += "\n{0} version: {1}".format(str(module), module.__version__)
		for module in self.plugins_classes:
			parent_module = sys.modules[module.__module__]
			version = parent_module.__version__ if hasattr(parent_module, '__version__') else 'Undefined'
			msg += "\n{0}:\t\t{1}".format(str(module.__name__), version)
		self.about(msg, "About {0}".format(self.title))

	def _edit_user_settings(self):
		try:
			if not hasattr(self, '_user_settings_editor'):
				user_settings_path = pkgutil.get_loader("pyforms_generic_editor_user_settings").get_filename()
				self._user_settings_editor = GenericFileEditor(user_settings_path, "user settings editor")
				self._user_settings_editor.set_cursor_position(conf.GENERIC_EDITOR_LOAD_EXCEPTION_LINE - 3, 0)
			self.mdi_area += self._user_settings_editor
		except Exception as err:
			logger.warning("User settings file not found")
			self.warning("User settings file doesn't exist.", "Cannot edit settings file")

	def _show_app_log(self):
		try:
			if not hasattr(self, '_app_log_editor'):
				app_log_path = "app.log"
				self._app_log_editor = GenericFileEditor(app_log_path, "app.log", read_only=False)
				self._app_log_editor.editor._code_editor.setCursorPosition(
					self._app_log_editor.editor._code_editor.lines() - 15, 0)
			self.mdi_area += self._app_log_editor
		except FileNotFoundError as err:
			logger.warning("User settings file not found: %s", os.path.realpath(app_log_path))
			self.warning("Log file doesn't exist.", "Cannot show app log file")

	def _exit_app(self):
		"""
		Exit app option from the menu
		"""
		qApp.quit()
