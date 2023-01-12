# !/usr/bin/python3
# -*- coding: utf-8 -*-

from confapp import conf

from pybpodgui_plugin.models.setup.setup_uibusy import SetupUIBusy

Setup = type(
    'Setup',
    tuple(conf.GENERIC_EDITOR_PLUGINS_FINDER.find_class('models.setup.Setup') + [SetupUIBusy]),
    {}
)
