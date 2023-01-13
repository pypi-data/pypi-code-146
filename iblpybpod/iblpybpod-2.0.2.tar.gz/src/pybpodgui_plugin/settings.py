# # !/usr/bin/python3
# # -*- coding: utf-8 -*-

import logging, os

SETTINGS_PRIORITY = 100



# THESE SETTINGS ARE NEEDED FOR PYSETTINGS
APP_LOG_FILENAME = 'app.log'
APP_LOG_HANDLER_CONSOLE_LEVEL = logging.WARNING
APP_LOG_HANDLER_FILE_LEVEL 	  = logging.WARNING

CONTROL_EVENTS_GRAPH_DEFAULT_SCALE 	= 100
BOARD_LOG_WINDOW_REFRESH_RATE 		= 1000

USE_MULTIPROCESSING = True

PYFORMS_MAINWINDOW_MARGIN 		= 0
PYFORMS_STYLESHEET 				= ''
PYFORMS_STYLESHEET_DARWIN 		= ''
PYFORMS_SILENT_PLUGINS_FINDER 	= True


#PYFORMS_STYLESHEET = os.path.join(os.path.dirname(__file__), 'resources', 'css', 'default.css')

PYFORMS_MATPLOTLIB_ENABLED 	= True
PYFORMS_WEB_ENABLED 		= True
PYFORMS_GL_ENABLED 			= True
PYFORMS_VISVIS_ENABLED 		= False

GENERIC_EDITOR_PLUGINS_PATH = None
GENERIC_EDITOR_PLUGINS_LIST = [
    'pybpodgui_plugin',
    'pybpodgui_plugin_timeline',
    'pybpodgui_plugin_trial_timeline',
    'pybpod_alyx_plugin',
    'pybpodgui_plugin_session_history',
#	'pge_welcome_plugin',
]

#WELCOME_PLUGIN_URL = 'http://pybpod.readthedocs.io'


############ BPODGUI PLUGIN SETTINGS ############

#DEFAULT_PROJECT_PATH = '/home/ricardo/bitbucket/pybpod/pybpod-gui-plugin/projects/Untitled project 1'

BOARD_LOG_WINDOW_REFRESH_RATE  = 2000
SESSIONLOG_PLUGIN_REFRESH_RATE = 1000
TIMELINE_PLUGIN_REFRESH_RATE   = 1000

PYBOARD_COMMUNICATION_THREAD_REFRESH_TIME  = 2 # timer for thread look for events (seconds)
PYBOARD_COMMUNICATION_PROCESS_REFRESH_TIME = 2 # timer for process look for events (seconds)
PYBOARD_COMMUNICATION_PROCESS_TIME_2_LIVE  = 0 # wait before killing process (seconds)

GENERIC_EDITOR_TITLE = 'PyBpod'


PYBPOD_REPOSITORIES_TXT_LIST = 'repositories.yml'