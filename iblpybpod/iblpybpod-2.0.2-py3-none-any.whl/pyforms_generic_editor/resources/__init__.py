# !/usr/bin/python3
# -*- coding: utf-8 -*-

import os


def path(filename):
	return os.path.join(os.path.dirname(__file__), 'icons', filename)


ADD_SMALL_ICON = path('add.png')
NEW_SMALL_ICON = path('new.png')
OPEN_SMALL_ICON = path('open.png')
SAVE_SMALL_ICON = path('save.png')
EXIT_SMALL_ICON = path('exit.png')
CLOSE_SMALL_ICON = path('close.png')
USER_SETTINGS_ICON = path('settings.png')

PLAY_SMALL_ICON = path('play.png')
BUSY_SMALL_ICON = path('busy.png')
PROJECT_SMALL_ICON = path('project.png')
REMOVE_SMALL_ICON = path('remove.png')

APP_LOGO_ICON = path('cf-original.png')
