# !/usr/bin/python3
# -*- coding: utf-8 -*-

from confapp import conf
from pybpodgui_plugin.models.projects.projects_treenode import ProjectsTreeNode

Projects = type(
    'Projects',
    tuple(conf.GENERIC_EDITOR_PLUGINS_FINDER.find_class('models.project.Projects') + [ProjectsTreeNode]),
    {}
)
