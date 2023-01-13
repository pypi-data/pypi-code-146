# !/usr/bin/python3
# -*- coding: utf-8 -*-

from confapp import conf

from pybpodgui_plugin.models.session.session_uibusy import SessionUIBusy

Session = type(
    'Session',
    tuple(conf.GENERIC_EDITOR_PLUGINS_FINDER.find_class('models.session.Session') + [SessionUIBusy]), {}
)
