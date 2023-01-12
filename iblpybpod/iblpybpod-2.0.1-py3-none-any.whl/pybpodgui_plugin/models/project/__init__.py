# !/usr/bin/python3
# -*- coding: utf-8 -*-
from confapp import conf
from pybpodgui_plugin.models.project.project_uibusy import ProjectUIBusy

Project = type(
    'Project',
    tuple(conf.GENERIC_EDITOR_PLUGINS_FINDER.find_class('models.project.Project') + [ProjectUIBusy]),
    {}
)
