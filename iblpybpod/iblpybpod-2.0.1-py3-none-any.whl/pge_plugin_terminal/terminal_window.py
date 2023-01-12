# !/usr/bin/python3
# -*- coding: utf-8 -*-

""" session_window.py

"""

import logging, sys, io, traceback
from confapp import conf
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlButton
from pyforms.controls import ControlText
from pyforms.controls import ControlTextArea
from pyforms.controls import ControlList

from confapp import conf

from AnyQt import QtCore
from AnyQt.QtWidgets import QFileDialog


logger = logging.getLogger(__name__)


class TerminalWindow(BaseWidget):
	""" ProjectWindow represents the project entity as a GUI window"""

	def __init__(self, projects):
		BaseWidget.__init__(self, 'Terminal')

		self.projects  = projects

		self._log      = ControlList()
		self._command  = ControlText('Command')
		self._exec_script_btn = ControlButton('Open & run a script')

		self._formset = [
			'_log',
			('_command', '_exec_script_btn')
		]

		self._log.word_wrap = True
		self._log.readOnly = True
		self._command.key_pressed_event = self.__command_key_pressed_evt

		self._exec_script_btn.value = self.open_and_run_script


	def open_and_run_script(self, filepath=None, extra_args={}):
		if not filepath:
			filepath = QFileDialog.getOpenFileName(self, 'OpenFile')
		if filepath:

			sys.stdout 				 = io.StringIO()
			self._locals['projects']  = self.projects
			self._locals.update(extra_args)
			try:
				self._log += (">> EXECUTE SCRIPT: {0}".format(filepath), )
				with open(filepath) as f:
					code = compile(f.read(), filepath, 'exec')
					exec(code, self._globals, self._locals)
			except:
				print(traceback.format_exc(),)
				
			self._log +=  (sys.stdout.getvalue(), )
			sys.stdout = sys.__stdout__

			self._log.resize_rows_contents()

		
	def show(self):
		# Prevent the call to be recursive because of the mdi_area
		if hasattr(self, '_show_called'):
			BaseWidget.show(self)
			return
		self._show_called = True
		self.mainwindow.mdi_area += self
		del self._show_called

		self._locals = locals()
		self._globals = globals()

	def beforeClose(self):	return False

	@property
	def mainwindow(self): return self.projects.mainwindow

	def execute_script(self, code, locals_vars, globals_vars):
		sys.stdout 				 = io.StringIO()
		locals_vars['projects']  = self.projects
		try:
			for line in code.split('\n'): 
				self._log += (">> {0}".format(line), )				
				exec(line, globals_vars, locals_vars)
		except:
			print(traceback.format_exc(),)
			
		self._log +=  (sys.stdout.getvalue(), )
		sys.stdout = sys.__stdout__

		self._log.resize_rows_contents()


	def __command_key_pressed_evt(self, event):
		if event.key() == QtCore.Qt.Key_Return:
			self.execute_script(self._command.value, self._locals, self._globals )
			self._command.value = ''
