# !/usr/bin/python3
# -*- coding: utf-8 -*-
import logging, os

SETTINGS_PRIORITY = 999

from pyforms_gui.utils.plugins_finder import PluginsFinder

GENERIC_EDITOR_MODEL = "pyforms_generic_editor.models.projects.Projects"
GENERIC_EDITOR_TITLE = "Set the variable GENERIC_EDITOR_TITLE in your settings file to change the title"

GENERIC_EDITOR_PLUGINS_PATH = None
GENERIC_EDITOR_PLUGINS_LIST = []

GENERIC_EDITOR_WINDOW_GEOMETRY = 100, 100, 1200, 800

GENERIC_EDITOR_PLUGINS_FINDER = PluginsFinder()

PYFORMS_STYLESHEET = ''
PYFORMS_STYLESHEET_DARWIN = ''

APP_LOG_FILENAME = 'app.log'
APP_LOG_HANDLER_FILE_LEVEL = logging.DEBUG
APP_LOG_HANDLER_CONSOLE_LEVEL = logging.INFO

PYFORMS_LOG_HANDLER_FILE_LEVEL = logging.DEBUG
PYFORMS_LOG_HANDLER_CONSOLE_LEVEL = logging.INFO

DEFAULT_PROJECT_PATH = None
