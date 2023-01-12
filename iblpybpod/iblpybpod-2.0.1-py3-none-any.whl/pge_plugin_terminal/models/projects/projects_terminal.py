# !/usr/bin/python3
# -*- coding: utf-8 -*-
from confapp import conf
from AnyQt.QtGui import QIcon

from pge_plugin_terminal.terminal_window import TerminalWindow

class ProjectsTerminal(object):

	def register_on_main_menu(self, mainmenu):
		super(ProjectsTerminal, self).register_on_main_menu(mainmenu)

		menu_index = 0
		for i, m in enumerate(mainmenu):
			if 'Window' in m.keys(): menu_index=i; break

		mainmenu[menu_index]['Window'].append( '-' )	
		mainmenu[menu_index]['Window'].append( {'Terminal': self.open_terminal_plugin, 'icon': conf.TERMINAL_PLUGIN_ICON} )
	
	def open_terminal_plugin(self):
		if not hasattr(self, 'terminal_plugin'):
			self.terminal_plugin = TerminalWindow(self)
			self.terminal_plugin.show()
			self.terminal_plugin.subwindow.resize(*conf.TERMINAL_PLUGIN_WINDOW_SIZE)			
		else:
			self.terminal_plugin.show()

		return self.terminal_plugin