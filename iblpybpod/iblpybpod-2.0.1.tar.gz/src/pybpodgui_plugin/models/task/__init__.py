# !/usr/bin/python3
# -*- coding: utf-8 -*-

from confapp import conf

from pybpodgui_plugin.models.task.task_dockwindow import TaskDockWindow

Task = type(
    'Task',
    tuple(conf.GENERIC_EDITOR_PLUGINS_FINDER.find_class('models.task.Task') + [TaskDockWindow]),
    {}
)
