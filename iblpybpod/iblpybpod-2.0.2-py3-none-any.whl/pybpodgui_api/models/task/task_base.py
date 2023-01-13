# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import os
import uuid

from pybpodgui_api.utils.generate_name import generate_name

from .taskcommand import ExecCmd, ScriptCmd

logger = logging.getLogger(__name__)


class TaskBase(object):
    """ Represents a state machine """

    def __init__(self, project=None):
        """
        :ivar Project project: Project to which the Task belongs to.
        """
        self.trigger_softcodes = False

        self.uuid4 = uuid.uuid4()
        self.filepath = None
        self.project = project
        self.name = generate_name([x.name for x in project.tasks], "task") if project else None
        self.project += self

        self._commands = []

    ##########################################################################
    ####### PROPERTIES #######################################################
    ##########################################################################

    @property
    def name(self):
        """
        Get and set task name

        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, value):
        previous_name = self._name if hasattr(self, '_name') else None
        previous_path = self.path if hasattr(self, '_name') else None

        self._name = value
        if previous_path is not None and self.filepath is not None:
            filepath = os.path.join(previous_path, self.name+'.py')
            os.rename(self.filepath, filepath)

            oldfilepath = os.path.join(previous_path, previous_name+'.json')
            filepath = os.path.join(previous_path, self.name+'.json')
            if os.path.isfile(oldfilepath):
                os.rename(oldfilepath, filepath)

            os.rename(previous_path, self.path)
            self.filepath = os.path.join(self.path, self.name+'.py')

    @property
    def path(self):
        """
        Get and set task path

        :rtype: str
        """
        if self.project.path is None:
            return None
        return os.path.join(self.project.path, 'tasks', self.name)

    @property
    def filepath(self):
        """
        Get and set task file path

        :rtype: str
        """
        return self._filepath

    @filepath.setter
    def filepath(self, value):
        self._filepath = value

    @property
    def project(self):
        """
        Get and set project

        :rtype: Project
        """
        return self._project

    @project.setter
    def project(self, project):
        self._project = project

    @property
    def trigger_softcodes(self):
        """
        Get net port

        :rtype: int
        """
        return self._trigger_softcodes

    @trigger_softcodes.setter
    def trigger_softcodes(self, value):
        self._trigger_softcodes = value

    @property
    def commands(self):
        """
        Get commands

        :rtype: list(TaskCommand)
        """
        return self._commands

    @commands.setter
    def commands(self, commands):
        """
        Setter for commands
        :param commands:
        :return:
        """
        self._commands = commands

    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    def make_path(self):
        """
        Creates the task folder
        """
        tasks_path = os.path.join(self.project.path, 'tasks')
        if not os.path.exists(tasks_path):
            os.makedirs(tasks_path)
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        open(os.path.join(self.path, '__init__.py'), 'w').close()

    def make_emptyfile(self):
        """
        Creates the task folder if does not exists and an empty code file
        """
        self.make_path()
        filepath = os.path.join(self.path, self.name+'.py')
        open(filepath, 'w').close()
        return filepath

    def create_scriptcmd(self):
        return ScriptCmd(self)

    def create_execcmd(self):
        return ExecCmd(self)

    def __add__(self, obj):
        if isinstance(obj, ScriptCmd):
            self._commands.append(obj)

        if isinstance(obj, ExecCmd):
            self._commands.append(obj)

        return self

    def __sub__(self, obj):
        if isinstance(obj, ScriptCmd):
            self._commands.remove(obj)

        if isinstance(obj, ExecCmd):
            self._commands.remove(obj)

        return self

    def remove(self):
        """
        Remove the task from the project.
        """
        pass

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()
