# !/usr/bin/python
# -*- coding: utf-8 -*-

import loggingbootstrap
import logging
import traceback
import sys
from importlib.util import find_spec

try:
	from confapp import conf

	# Initiating logging for pyforms. It has to be initiated manually here because we don't know yet
	# the logger filename as specified on settings
	loggingbootstrap.create_double_logger("pyforms", logging.INFO, 'app.log', logging.INFO)

except ImportError as err:
	logging.getLogger().critical(str(err), exc_info=True)
	exit("Could not load pyforms! Is it installed?")

# CHECK IF PYFORMS IS AVAILABLE WITHOUT ACTUALLY IMPORTING IT
pyforms_spec = find_spec("pyforms")
if not pyforms_spec:
	exit("Could not load pyforms! Is it installed?")

try:
	# pyforms is imported here first time through pyforms
	from pyforms_generic_editor import settings

	import user_settings

	conf += user_settings

	loggingbootstrap.create_double_logger("pyforms_generic_editor", conf.APP_LOG_HANDLER_CONSOLE_LEVEL,
	                                      conf.APP_LOG_FILENAME,
	                                      conf.APP_LOG_HANDLER_FILE_LEVEL)

	loggingbootstrap.create_double_logger("pyforms", conf.PYFORMS_LOG_HANDLER_CONSOLE_LEVEL, conf.APP_LOG_FILENAME,
	                                      conf.PYFORMS_LOG_HANDLER_FILE_LEVEL)

	# pyforms.controls is imported here first time
	from pyforms_generic_editor.editor.base_editor import BaseEditor as Editor

except Exception as err:
	exc_type, exc_value, exc_traceback = sys.exc_info()
	logging.getLogger("pyforms_generic_editor").critical(str(err), exc_info=True)
	conf.GENERIC_EDITOR_LOAD_EXCEPTION_TRACEBACK = traceback.format_exc()
	conf.GENERIC_EDITOR_LOAD_EXCEPTION_LINE = exc_traceback.tb_lineno
	settings.GENERIC_EDITOR_TITLE = 'PLEASE EDIT USER SETTINGS AND RESTART APP'
	from pyforms_generic_editor.editor.safe_mode_editor import SafeModeEditor as Editor


def start():
	import pyforms
	pyforms.start_app(Editor, conf.GENERIC_EDITOR_WINDOW_GEOMETRY)


if __name__ == '__main__':
	start()
